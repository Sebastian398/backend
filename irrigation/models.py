import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Sensor(models.Model):
    tipo = models.CharField(max_length=50)  # e.g. humedad, temperatura
    valor = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.valor}'

class ProgramacionRiego(models.Model):
    inicio = models.TimeField()
    duracion = models.IntegerField(help_text='Duración en minutos')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'Riego a las {self.inicio} por {self.duracion} min'


def fecha_expiracion_default():
    return timezone.now() + timedelta(days=2)

class ActivacionUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField(default=fecha_expiracion_default)
    def esta_expirado(self):
        return timezone.now() > self.expiracion

    def __str__(self):
        return f"Token de activacion para {self.user.email}"
    
# from rest_framework import viewsets
#from .models import Sensor, ProgramacionRiego
#from .serializers import SensorSerializer, ProgramacionRiegoSerializer
#from rest_framework.decorators import action
#from rest_framework.response import Response

#import RPi.GPIO as GPIO
#import time

#RELAY_PIN = 17
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(RELAY_PIN, GPIO.OUT)
#GPIO.output(RELAY_PIN, GPIO.LOW)

#class SensorViewSet(viewsets.ModelViewSet):
#    queryset = Sensor.objects.all().order_by('-fecha_registro')
#    serializer_class = SensorSerializer

#class ProgramacionRiegoViewSet(viewsets.ModelViewSet):
#    queryset = ProgramacionRiego.objects.filter(activo=True)
#    serializer_class = ProgramacionRiegoSerializer

#    @action(detail=True, methods=['post'])
#    def activar_riego(self, request, pk=None):
#        programacion = self.get_object()
#        duracion_minutos = programacion.duracion
#        duracion_segundos = duracion_minutos * 60  # Convierte minutos a segundos
        
#        try:
#            GPIO.output(RELAY_PIN, GPIO.HIGH)
#            time.sleep(duracion_segundos)
#            GPIO.output(RELAY_PIN, GPIO.LOW)

#            mensaje = f'Riego activado por {duracion_minutos} minutos correctamente.'
#            return Response({'mensaje': mensaje})

#        except Exception as e:
#            GPIO.output(RELAY_PIN, GPIO.LOW)
#            return Response({'error': f'Error al activar riego: {str(e)}'}, status=500)
