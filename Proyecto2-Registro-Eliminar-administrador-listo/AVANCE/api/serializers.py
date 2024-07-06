from rest_framework import serializers
from core.models import Planta, Producto, Produccion

class ProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produccion
        fields = '__all__'

class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
