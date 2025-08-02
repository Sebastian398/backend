from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from .views import SensorViewSet, ProgramacionRiegoViewSet, RegisterView, AccesoValidateView, CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView


# Router para viewsets de sensores y programacion_riego
router = DefaultRouter()
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'programacion_riego', ProgramacionRiegoViewSet, basename='programacion_riego')


# Vista raíz personalizada para que aparezcan todos los endpoints
class ApiRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'register': request.build_absolute_uri('register/'),
            'login': request.build_absolute_uri('login/'),
            'token_refresh': request.build_absolute_uri('token/refresh/'),
            'sensores': request.build_absolute_uri('sensores/'),
            'programacion_riego': request.build_absolute_uri('programacion_riego/'),
        })


urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),          # /api/
    path('register/', RegisterView.as_view(), name='register'), # /api/register/
    path('login/', CustomLoginView.as_view(), name='login'),          # /api/login/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # /api/token/refresh/
    path('api/acceso-validate/', AccesoValidateView.as_view(), name='acceso-validate'),
    path('', include(router.urls)),                              # /api/sensores/, /api/programacion_riego/
]
