from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Sensor, ProgramacionRiego, ActivacionUsuario
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from .serializers import (
    SensorSerializer,
    ProgramacionRiegoSerializer,
    UserRegisterSerializer,
    EmailTokenObtainPairSerializer,
    UserDetailSerializer,
    ProgramacionRiegoAdminSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Crear token de activación
            token_obj = ActivacionUsuario.objects.create(user=user)

            # Construir URL absoluto para activar cuenta
            url_activacion = request.build_absolute_uri(
                reverse('activar-cuenta', kwargs={'token': str(token_obj.token)})
            )

            # Enviar email de activación
            asunto = 'Activa tu cuenta'
            mensaje = f'Hola {user.first_name}, gracias por registrarte. Por favor activa tu cuenta haciendo click en el siguiente enlace: {url_activacion}'
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"mensaje": "Registro exitoso. Revisa tu email para activar la cuenta."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Error en el registro", "detalles": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class ActivarCuentaView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):
        token_obj = get_object_or_404(ActivacionUsuario, token=token)
        
        if token_obj.esta_expirado():
            return Response({'error': 'El enlace de activación expiró.'}, status=status.HTTP_400_BAD_REQUEST)

        user = token_obj.user
        user.is_active = True
        user.save()

        token_obj.delete()

        return Response({'mensaje': 'Cuenta activada exitosamente.'}, status=status.HTTP_200_OK)

class CustomLoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return Response({
                "error": "Credenciales inválidas",
                "detalles": exc.detail
            }, status=status.HTTP_401_UNAUTHORIZED)

        data = serializer.validated_data
        email = request.data.get('email', '')

        password_reset_url = request.build_absolute_uri('/api/password_reset/')
        return Response({
            "mensaje": f"¡Bienvenido, {email}!",
            "access": data.get("access"),
            "refresh": data.get("refresh"),
            "password_reset_url": password_reset_url
        })


class AccesoValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"mensaje": "Acceso concedido. Token válido y autenticación correcta."})


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all().order_by('-fecha_registro')
    serializer_class = SensorSerializer

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        sensor = self.get_object()
        sensor.activo = True
        sensor.save()
        return Response({'mensaje': 'Rociador activado'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        sensor = self.get_object()
        sensor.activo = False
        sensor.save()
        return Response({'mensaje': 'Rociador desactivado'}, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
class ProgramacionRiegoViewSet(viewsets.ModelViewSet):
    queryset = ProgramacionRiego.objects.filter(activo=True)
    serializer_class = ProgramacionRiegoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def activar_riego(self, request, pk=None):
        programacion = self.get_object()
        # Aquí podrías agregar la lógica real para activar el riego mediante hardware

        return Response({'mensaje': f'Riego activado por {programacion.duracion} minutos'})

class ProgramacionRiegoAdminViewSet(viewsets.ModelViewSet):
    """
    Endpoint para listar, modificar y eliminar todas las programaciones de riego,
    sin filtrado (todas activas e inactivas).
    """
    queryset = ProgramacionRiego.objects.all().order_by('-inicio')
    serializer_class = ProgramacionRiegoAdminSerializer
    permission_classes = [IsAuthenticated]
