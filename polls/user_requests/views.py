from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from django.http import JsonResponse
from polls.models import *
from rest_framework.permissions import IsAuthenticated 
from .serializers import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservepost_cancel(request):

    user=request.user
    data=request.data
    date=data['date']
    pid=data['pid']
    rid=data['rid']
    reservation=Reservation.objects.get(id=rid)
    substitute_user=User.objects.get(id=pid)
    person_wantcancel=Profile.objects.get(user=user)
    person_substitute=Profile.objects.get(user=substitute_user)
    
    r=Res_Done.objects.filter(reservation=reservation,date=date,user=user)
    rr=Res_Done_Op.objects.filter(reservation=reservation,date=date,user=user,op_leader=False)
    rrr=Res_Done_Op.objects.filter(reservation=reservation,date=date,user=user,op_leader=True)
    if r.exists():
        location=r[0].location
        type="اسعاف"
    elif rr.exists():
        location=rr[0].location
        type="عمليات"
    elif rrr.exists():
        location=rrr[0].location
        type="قائد قطاع " 
     
    if r or rr or rrr:
        try:
            if Cancel_Request.objects.filter(person_wantcancel=user,
            person_substitute=substitute_user,
            reservation=reservation,
            date=date).exists():
                error=Error_Message.objects.get(name="Duplicate")
                return JsonResponse({'result':error.message})       
            Cancel_Request.objects.create(person_wantcancel=user,
            person_substitute=substitute_user,
            reservation=reservation,
            type=type,
            location=location,
            person_wantcancel_name=person_wantcancel.fullName,
            person_substitute_nam=person_substitute.fullName,
            date=date,
            shift_time=reservation.shift_time,
            )
            error=Error_Message.objects.get(name="request done")
            return JsonResponse({'result':error.message}) 
        except:
                error=Error_Message.objects.get(name="ID not found")
                return JsonResponse({'result':error.message}) 
    else:
        error=Error_Message.objects.get(name="book not found")
        return JsonResponse({'result':error.message})               

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reservepost_repair(request):

    data=request.data
    user=request.user
    rid=data['rid']
    type=data['type']
    location=data['location']
    date=data['date']

    reservation=Reservation.objects.get(id=rid)
    person_wantrepair=Profile.objects.get(user=user)
    c=control_center.objects.get(location=location)

    r=Res_Done.objects.filter(user=user,date=date,reservation=reservation)
    rr=Res_Done_Op.objects.filter(user=user,date=date,reservation=reservation)
    if r or rr:
        error=Error_Message.objects.get(name="booked")
        return JsonResponse({'result':error.message}) 

    if (type=="عمليات" and  person_wantrepair.operations==False) or (type=="قائد قطاع" and person_wantrepair.op_leader==False) :
        error=Error_Message.objects.get(name="opereations False")
        return JsonResponse({'result':error.message}) 
    max=0    
    if person_wantrepair.rank=="sought":
        max=c.sought_max
    elif  person_wantrepair.rank=="scout":
        max=c.scout_max    
    elif  person_wantrepair.rank=="leader":  
         max=c.leader_max 

    if type=="اسعاف" and( Res_Done.objects.filter(reservation=reservation,date=date,location=location).count() >=c.team_max_amb or Res_Done.objects.filter(reservation=reservation,date=date,rank=person_wantrepair.rank,location=location).count()>=max):
        error=Error_Message.objects.get(name="vacant not found")
        return JsonResponse({'result':error.message}) 

    if type=="عمليات" and( Res_Done_Op.objects.filter(reservation=reservation,date=date,location=location,op_leader=False).count() >=c.team_max_ob):
        error=Error_Message.objects.get(name="vacant not found")
        return JsonResponse({'result':error.message}) 

    if type=="قائد قطاع" and ( Res_Done_Op.objects.filter(reservation=reservation,date=date,location=location,op_leader=True).count() >=1):    
        error=Error_Message.objects.get(name="vacant not found")
        return JsonResponse({'result':error.message}) 
  
    if Repair_Request.objects.filter(type=type,
    location=location,
    user=user,
    reservation=reservation,
    date=date).exists:
        error=Error_Message.objects.get(name="Duplicate")
        return JsonResponse({'result':error.message})          


    Repair_Request.objects.create(person_wantrepair=user,
            reservation=reservation,
            type=type,
            location=location,
            person_wantrepair_name=person_wantrepair.fullName,
            date=date,
            shift_time=reservation.shift_time,
            )    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def query_about_cancel(request):
 #if isNowInTimePeriod(dt.time(20,00), dt.time(23,30), timezone.now().time()):
  user=request.user
  date = datetime.datetime.now()
  q=Cancel_Request.objects.filter(person_wantcancel=user,date__gte=date)
  serializer=Cancel_RequestSerializer(q,many=True)
  return JsonResponse(serializer.data,safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def query_about_repair(request):
 #if isNowInTimePeriod(dt.time(20,00), dt.time(23,30), timezone.now().time()):
  user=request.user
  date = datetime.datetime.now()
  q=Repair_Request.objects.filter(person_wantrepair=user,date__gte=date)
  serializer=Repair_RequestSerializer(q,many=True)
  return JsonResponse(serializer.data,safe=False)     