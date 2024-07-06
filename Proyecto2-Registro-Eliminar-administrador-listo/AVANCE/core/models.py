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
        return self.nombre

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
    hora_registro=models.DateTimeField(auto_now_add=True)
    operador= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha_produccion} - {self.turno} "
    