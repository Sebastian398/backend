from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from .views import SensorViewSet, ProgramacionRiegoViewSet, RegisterView, AccesoValidateView, CustomLoginView, UserDetailView, ProgramacionRiegoAdminViewSet, ActivarCuentaView, RegistroRiegoViewSet, LecturasHumedadList, EstadisticasHumedadSemanal
from rest_framework_simplejwt.views import TokenRefreshView


# Router para viewsets de sensores y programacion_riego
router = DefaultRouter()
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'programacion_riego', ProgramacionRiegoViewSet, basename='programacion_riego')
router.register(r'programacion_riego_admin', ProgramacionRiegoAdminViewSet, basename='programacionriegoadmin')
router.register(r'registro_riego', RegistroRiegoViewSet, basename='registro_riego')

class ApiRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'register': request.build_absolute_uri('register/'),
            'login': request.build_absolute_uri('login/'),
            'token_refresh': request.build_absolute_uri('token/refresh/'),
            'sensores': request.build_absolute_uri('sensores/'),
            'datos': request.build_absolute_uri('usuario-actual/'),
            'programacion_riego': request.build_absolute_uri('programacion_riego/'),
            'programacion_riego_admin': request.build_absolute_uri('programacion_riego_admin/'),
        })


urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),          
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', CustomLoginView.as_view(), name='login'),          
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('api/acceso-validate/', AccesoValidateView.as_view(), name='acceso-validate'),
    path('usuario-actual/', UserDetailView.as_view(), name='usuario-actual'),
    path('activar-cuenta/<uuid:token>/', ActivarCuentaView.as_view(), name='activar-cuenta'),
    path('lecturas_humedad/', LecturasHumedadList.as_view(), name='lecturas-humedad'),
    path('estadisticas_humedad_semanal/', EstadisticasHumedadSemanal.as_view(), name='estadisticas-humedad-semanal'),
    path('', include(router.urls)),                              
]
