from rest_framework import serializers
from .models import Sensor, ProgramacionRiego

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class ProgramacionRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionRiego
        fields = '__all__'
