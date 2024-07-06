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
    planta = serializers.CharField(source='planta.nombre', read_only=True)

    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'litros_totales', 'planta']
