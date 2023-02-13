
from django.contrib.auth.models import User  
from django.shortcuts import render
from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from django.http import JsonResponse
from polls.views import *
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated 
from rest_framework import generics
# from django.contrib.auth import get_user_model
# from django.http import HttpResponse   
# from django.contrib.sites.shortcuts import get_current_site  
# from django.utils.encoding import force_bytes, force_text  
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
# from django.template.loader import render_to_string  
# from .tokens import account_activation_token  
from django.contrib.auth.models import User  
# from django.core.mail import EmailMessage  

from .serializers import *
import requests

import shortuuid




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        data["detail"]="ok"
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer 


@api_view(['POST'],)
@authentication_classes([])
@permission_classes([])
def signup(request):  
    # try:

            data = request.data  
            email=data['email']
            phoneNumber=data['phoneNumber']
            gender=data['gender']
            rank=data['rank']
            operations=data['operations']
            op_leader=data['op_leader']
            fullName=data['fullName']
            code64=data['image']
    
             
            if User.objects.filter(email__icontains=email,is_active=True).exists() or Profile.objects.filter(phone=phoneNumber,is_verified=True).exists() or User.objects.filter(username__icontains=data['username'],is_active=True).exists() or Profile.objects.filter(fullName=fullName,is_verified=True).exists() :
                message = {'detail': 'User with this phonenumber or username already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            join_list=Join_Request.objects.all()
            for i in join_list:
                user=i.user
                if user.email==email or user.username==data['username'] or i.fullName==fullName:
                    message = {'detail': 'User with this phonenumber or username already exists'}
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                else:
                    continue
            else: 
                if User.objects.filter(email__icontains=email,is_active=False).exists()    :
                    User.objects.filter(email__icontains=email,is_active=False).delete()
                if  User.objects.filter(username__icontains=data['username'],is_active=False).exists():
                    User.objects.filter(username__icontains=data['username'],is_active=False).delete()
                p=Profile.objects.filter(phone=phoneNumber,is_verified=False)   
                if      p.exists():
                    user=p[0].user
                    user.delete()

                user = User.objects.create(
                    username=data['username'],
                    email=data['email'],
                    password=make_password(data['password']) ,
                    is_active  =False
                ) 
                # to get the domain of the current site  
                s = shortuuid.ShortUUID(alphabet="0123456789")
                otp = s.random(length=6)
                message=" كود التفعيل الخاص بك هو" + otp
                send_sms(message,phoneNumber)

 
                image=convert_base64(code64,data['username'],otp)

                p=Profile.objects.get(user=user)
                p.phone=phoneNumber
                p.gender=gender
                p.rank=rank
                p.operations=operations
                p.op_leader=op_leader
                p.otp=otp
                p.fullName=fullName
                p.image=image
                p.save()

               
                message = {'detail': 'Please confirm your phoneNumber to complete the registration'}
                return Response(message)

    # except:
    #     message = {'detail': 'User with this email or username already exists'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])

def verify_otp(request):
    data=request.data
    otp=data['otp']
    p=Profile.objects.filter(otp=otp)
    try:
        if p[0].otp==otp:
            p[0].is_verified==True
            Join_Request.objects.create(user=p[0].user,fullName=p[0].fullName,
            gender=p[0].gender,
            rank=p[0].rank,
            operations=p[0].operations,
            op_leader=p[0].op_leader,
            phone=p[0].phone,
            image=p[0].image)
            Profile.objects.filter(otp=otp).update(is_verified=True,otp="")
            return JsonResponse("successfully",safe=False)
    except:
        return JsonResponse("wrong otp",safe=False)    



# @api_view(['POST'],)
# @authentication_classes([])
# @permission_classes([])
# def signup(request):  
#     try:
 
#             data = request.data  
#             email=data['email']
#             phoneNumber=data['phoneNumber']
#             gender=data['gender']
#             rank=data['rank']
#             operations=data['operations']
#             op_leader=data['op_leader']
            
#             # save form in the memory not in database  
#             if User.objects.filter(email__icontains=email).exists() or User.objects.filter(username__icontains=data['username']).exists()  :
#                 message = {'detail': 'User with this email or username already exists'}
#                 return Response(message, status=status.HTTP_400_BAD_REQUEST)
#             else:    
#                 user = User.objects.create(
#                     username=data['username'],
#                     email=data['email'],
#                     password=make_password(data['password']) ,
#                     is_active=False 
#                 ) 
       
#                 p=Profile.objects.get(user=user)
#                 p.phone=phoneNumber
#                 p.gender=gender
#                 p.rank=rank
#                 p.operations=operations
#                 p.op_leader=op_leader
#                 p.save()

                
#                 # to get the domain of the current site  
#                 current_site = get_current_site(request)  
                
#                 mail_subject = 'Activation link has been sent to your email id'  
#                 message = render_to_string('acc_active_email.html', {  
#                         'user': user,  
#                         'domain': current_site.domain,  
#                         'uid':urlsafe_base64_encode(force_bytes(user.pk)), 
#                         'token':account_activation_token.make_token(user),  
#                     })      
#                 to_email = data['email']
#                 email = EmailMessage(
#                                 mail_subject, message, to=[to_email]  
#                     )  
                
#                 email.send()  
#                 message = {'detail': 'Please confirm your email address to complete the registration'}
#                 return Response(message)

#     except:
        
#         message = {'detail': 'User with this email or username already exists'}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)


# def activate(request, uidb64, token):  
#     User = get_user_model()
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))  
#         user = User.objects.get(pk=uid)  
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
#         user = None  
#     pro=Profile.objects.get(user=user)    
#     if pro.is_verified == True:
#         user=None    
#     if user is not None and account_activation_token.check_token(user, token):  
        
#         pro.is_verified = True 
#         pro.save()  
#         Join_Request.objects.create(user=pro.user     ,
#         fullName=pro.fullName,
#         gender=pro.gender,
#         rank=pro.rank,
#         operations=pro.operations,
#         op_leader=pro.op_leader,
#         phone=pro.phone)
#         return HttpResponse('Thank you for your email confirmation. Now your account is verified')  
#     else:  
#         return HttpResponse('Activation link is invalid!')






class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            data=request.data
            old_password=data['old_password']
            password=data['password']
       
            
            
          
                # Check old password
            if not self.object.check_password(old_password):
                return Response({"message": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(password)
            self.object.save()
            response = {
              
                'message': 'Password updated successfully',
        
            }

            return Response(response)


