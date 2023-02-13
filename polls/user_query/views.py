 
from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from django.http import JsonResponse
from polls.models import *
from rest_framework.permissions import IsAuthenticated 
from .serializers import *
from polls.views import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def count_shift_post(request):
    
    user=request.user
    data=request.data
    month_num=int(data['month_num'])
    year_num=int(data['year_num'])
    
    count1=Res_Done.objects.filter(user=user,date__month=month_num,date__year=year_num).count()
    count2=Res_Done_Op.objects.filter(user=user,date__month=month_num,date__year=year_num).count()
    result={}
    result['message1']=count1
    result['message2']=count2
    return JsonResponse(result,safe=False)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def myreservations(request):

    user=request.user
    data=request.data
    a=[]
    month_num=int(data['month_num'])
    year_num=int(data['year_num'])
    type=data['type']
    if type=="اسعاف":
        res_done=Res_Done.objects.filter(user=user,date__month=month_num,date__year=year_num).order_by('date')
        serializer=Res_DoneSerializer(res_done,many=True)
        return Response(serializer.data)
    else:
        res_done_op=Res_Done_Op.objects.filter(user=user,date__month=month_num,date__year=year_num).order_by('date')
        serializer=Res_Done_OpSerializer(res_done_op,many=True)
        return Response(serializer.data)
   
    
    