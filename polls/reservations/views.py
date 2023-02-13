
from django.contrib.auth.models import User  
from rest_framework.response import Response
from polls.models import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from django.http import JsonResponse
from polls.models import *
from rest_framework.permissions import IsAuthenticated 
from .serializers import *
from .functions import *



@api_view(['GET'])
def  get_reservations(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def valid_reservation(request):
    user=request.user
    pid=user.id
    weekNumber="الأسبوع الأول"
    type="عمليات"
    team_max_amb=10
    sought_max=10
    leader_max=10
    scout_max=10
    female_max=2
    start_res_day=10
    team_max_ob=10
    team_max_ob_leader=1



    a=valid_reserve(pid,
    weekNumber,
    type,
    team_max_amb,
    sought_max,
    leader_max,
    scout_max,
    female_max,
    start_res_day,
    team_max_ob,
    team_max_ob_leader)
    return JsonResponse(a,safe=False)
@api_view(['post'])
@permission_classes([IsAuthenticated])
def reservepost(request):
    user=request.user
  
    type="عمليات"
    team_max_amb=10
    sought_max=10
    leader_max=10
    scout_max=10
    female_max=2
    start_res_day=10
    team_max_ob=10
    team_max_ob_leader=1
    location="320"

    check=reserve(user,
    type,
    location,
    team_max_amb,
    sought_max,
    leader_max,
    scout_max,
    female_max,
    start_res_day,
    team_max_ob,
    team_max_ob_leader)

    if check==True:
        return JsonResponse("Success",safe=False)
    else:
        return JsonResponse("fail",safe=False)

    
