from rest_framework import serializers
from polls.models import *

class Res_DoneSerializer(serializers.ModelSerializer):
    day_in_month=serializers.SerializerMethodField()
    shift_time=serializers.SerializerMethodField()
    class Meta:
        
        model=Res_Done
        fields= ('location','date','day_in_month','shift_time')

    def get_day_in_month(self, obj)  :
        r=Reservation.objects.get(id=obj.reservation.id)
        return r.day_in_month

    def get_shift_time(self, obj)  :   
        r=Reservation.objects.get(id=obj.reservation.id)
        return r.shift_time 

class Res_Done_OpSerializer(serializers.ModelSerializer):
    day_in_month=serializers.SerializerMethodField()
    shift_time=serializers.SerializerMethodField()
    class Meta:
        model=Res_Done_Op
        fields= ('location','date','day_in_month','shift_time')

    def get_day_in_month(self, obj)  :
        r=Reservation.objects.get(id=obj.reservation.id)
        return r.day_in_month

    def get_shift_time(self, obj)  :   
        r=Reservation.objects.get(id=obj.reservation.id)
        return r.shift_time 