from django.db import models
from django.contrib.auth.models import User
import requests
from django.conf import settings
from django.utils import timezone
import datetime
from dateutil import parser

class Planta(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=100)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    litros_totales = models.IntegerField(default=0)

    def __str__(self):
        return self.codigo

turnos = [
    ("AM", "Mañana"),
    ("PM", "Tarde"),
    ("MM", "Noche"),
]

class Produccion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Litros_producido = models.IntegerField()
    fecha_produccion = models.DateField()
    turno = models.CharField(max_length=100, choices=turnos)
    hora_registro = models.TimeField()
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    anulado = models.BooleanField(default=False)
    usuario_anulacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='producciones_anuladas')
    fecha_anulacion = models.DateTimeField(null=True, blank=True)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modificaciones')
    fecha_modificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.producto.codigo} - {self.fecha_produccion} - {self.turno} "
    
    #PA QUE NO SE ME OLVIDE ESTE VA ACTUALIZANDO LOS LITROS EN CASO QUE SE MODIFIQUE O SE ELIMINE Y ME HAGA LA SUMA TOTAL
    #ADEMAS PARA QUE ME MUESTRE LA SUMA TOTAL EN EL SLACK

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.actualizar_litros_totales()
        self.enviar_notificacion_slack()

    def delete(self, *args, **kwargs):
        producto = self.producto
        super().delete(*args, **kwargs)
        self.actualizar_litros_totales(producto)

    def actualizar_litros_totales(self, producto=None):
        if producto is None:
            producto = self.producto
        total_litros = Produccion.objects.filter(producto=producto, anulado=False).aggregate(total=models.Sum('Litros_producido'))['total']
        producto.litros_totales = total_litros if total_litros is not None else 0
        producto.save()
        print(f"Producto {producto.codigo} actualizado: {producto.litros_totales} litros")


 #esto envia a la aplicacion cuando hace un registro
    def enviar_notificacion_slack(self):
        pass

    def enviar_notificacion_slack(self):
        webhook_url = settings.SLACK_WEBHOOK_URL
        if not webhook_url:
            return

        # Me aseguro que la fecha y la hora sea la que ingreso desde el html
        if isinstance(self.fecha_produccion, str):
            self.fecha_produccion = parser.parse(self.fecha_produccion).date()
        if isinstance(self.hora_registro, str):
            self.hora_registro = parser.parse(self.hora_registro).time()

        fecha_hora = datetime.datetime.combine(self.fecha_produccion, self.hora_registro).strftime('%d-%m-%Y %H:%M')
        mensaje = (
            f"{fecha_hora} {self.producto.planta.codigo} – Nuevo Registro de Producción – "
            f"{self.producto.codigo} {self.Litros_producido} lts. | "
            f"Total Almacenado: {self.producto.litros_totales} lts."
        )
        payload = {"text": mensaje}
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            print(f"Error al enviar la notificación a Slack: {response.status_code}, {response.text}")