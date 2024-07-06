from rest_framework import viewsets
from core.models import Produccion, Producto, Planta
from .serializers import ProduccionSerializer, PlantaSerializer, ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# Custom filter for Produccion
class ProduccionFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(field_name="fecha_produccion", lookup_expr='year')
    mes = django_filters.NumberFilter(field_name="fecha_produccion", lookup_expr='month')

    class Meta:
        model = Produccion
        fields = ['ano', 'mes']

class ProduccionesViewSet(viewsets.ModelViewSet):
    queryset = Produccion.objects.all()
    serializer_class = ProduccionSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProduccionFilter

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer

# Vista personalizada
@api_view(['GET'])
def lista_productos(request):
    productos = Producto.objects.all()
    data = []
    for producto in productos:
        serializer = ProductoSerializer(producto)
        planta_info = {
            "Planta": producto.planta.nombre,
            "Producto": serializer.data
        }
        data.append(planta_info)
    return Response(data)
