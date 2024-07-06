from django.urls import path, include
from rest_framework import routers
from .views import ProduccionesViewSet, ProductoViewSet, PlantaViewSet, lista_productos

router = routers.DefaultRouter()
router.register('TotalDeProducciones', ProduccionesViewSet)
router.register('TipoDeCombustible', ProductoViewSet)
router.register('planta', PlantaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/productos/', lista_productos, name='lista_productos'),
]
