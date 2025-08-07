from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Sensor, ProgramacionRiego
from .serializers import (
    SensorSerializer,
    ProgramacionRiegoSerializer,
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"mensaje": "Registro exitoso. ¡Bienvenido!", "usuario": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Error en el registro", "detalles": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Credenciales inválidas", "detalles": serializer.errors},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "mensaje": f"¡Bienvenido, {user.first_name or user.username}!",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class AccesoValidateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"mensaje": "Acceso concedido. Token válido y autenticación correcta."})


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all().order_by('-fecha_registro')
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProgramacionRiegoViewSet(viewsets.ModelViewSet):
    queryset = ProgramacionRiego.objects.filter(activo=True)
    serializer_class = ProgramacionRiegoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def activar_riego(self, request, pk=None):
        programacion = self.get_object()
        # Aquí puedes agregar la lógica para activar el riego mediante hardware
        return Response({'mensaje': f'Riego activado por {programacion.duracion} minutos'})
