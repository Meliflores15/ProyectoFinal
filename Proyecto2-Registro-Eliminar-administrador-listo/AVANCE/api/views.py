from django.shortcuts import render
from rest_framework import serializers,viewsets
from core.models import Produccion, Producto, Planta
from .serializers import ProduccionSerializer, PlantaSerializer,ProductoSerializer
# Create your views here.

class ProduccionesViewSet(viewsets.ModelViewSet):
    queryset=Produccion.objects.all()
    #gestion de la informacion a mostrar por el api
    serializer_class=ProduccionSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer

class PlantaViewSet(viewsets.ModelViewSet):
    queryset=Planta.objects.all()
    serializer_class=PlantaSerializer
