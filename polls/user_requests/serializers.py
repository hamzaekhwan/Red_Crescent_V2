from rest_framework import serializers
from polls.models import *



class Cancel_RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cancel_Request
        fields= '__all__'

class Repair_RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Repair_Request
        fields= '__all__'        