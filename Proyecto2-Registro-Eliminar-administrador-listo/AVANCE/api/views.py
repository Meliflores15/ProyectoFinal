from rest_framework import viewsets
from core.models import Produccion, Producto, Planta
from .serializers import ProduccionSerializer, PlantaSerializer, ProductoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Definición de los ViewSets
class ProduccionesViewSet(viewsets.ModelViewSet):
    queryset = Produccion.objects.all()
    serializer_class = ProduccionSerializer

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
