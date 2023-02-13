from rest_framework import serializers
from polls.models import *



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields= '__all__'
