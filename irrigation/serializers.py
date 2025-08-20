from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Sensor, ProgramacionRiego


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}, label="Contraseña"
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}, label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Este email ya está registrado."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data['email']

        base_username = email.split('@')[0]
        username = base_username
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{get_random_string(4)}"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError({"detail": "Se deben proveer email y contraseña."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No existe un usuario con este email."})

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError({"password": "Contraseña incorrecta."})

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class ProgramacionRiegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionRiego
        fields = '__all__'
class ProgramacionRiegoAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramacionRiego
        fields = '__all__'