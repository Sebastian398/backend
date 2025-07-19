from rest_framework import viewsets
from .models import Sensor, ProgramacionRiego
from .serializers import SensorSerializer, ProgramacionRiegoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all().order_by('-fecha_registro')
    serializer_class = SensorSerializer

class ProgramacionRiegoViewSet(viewsets.ModelViewSet):
    queryset = ProgramacionRiego.objects.filter(activo=True)
    serializer_class = ProgramacionRiegoSerializer

    @action(detail=True, methods=['post'])
    def activar_riego(self, request, pk=None):
        # Aquí puedes agregar lógica para activar el riego físico via hardware o una cola
        programacion = self.get_object()
        return Response({'mensaje': f'Riego activado por {programacion.duracion} segundos'})
