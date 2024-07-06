from django.db import models
from django.contrib.auth.models import User


class Planta(models.Model):
    codigo= models.CharField(max_length=3)
    nombre= models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre

class Producto(models.Model):
    codigo= models.CharField(max_length=3)
    nombre= models.CharField(max_length=100)
    planta= models.ForeignKey(Planta, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.codigo

turnos=[
    ("AM","Mañana"),
    ("PM","Tarde"),
    ("MM","Noche"),
]
    

class Produccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Litros_producido= models.IntegerField()
    fecha_produccion = models.DateField()
    turno= models.CharField(max_length=100,choices=turnos)
    hora_registro = models.TimeField()
    operador= models.ForeignKey(User, on_delete=models.CASCADE)
    anulado = models.BooleanField(default=False)
    usuario_anulacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='producciones_anuladas')
    fecha_anulacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.producto.codigo} - {self.fecha_produccion} - {self.turno} "
    