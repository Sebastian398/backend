from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, ProgramacionRiegoViewSet

router = DefaultRouter()
router.register(r'sensores', SensorViewSet)
router.register(r'programacion_riego', ProgramacionRiegoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
