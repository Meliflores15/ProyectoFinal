from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Planta, Producto, Produccion
from django.utils import timezone
from django import forms
admin.site.register(Planta)
admin.site.register(Producto)

class ProduccionAdminForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios para mostrar solo los supervisores
        supervisores = Group.objects.get(name="Supervisores").user_set.all()
        self.fields['usuario_anulacion'].queryset = supervisores
        
#supervisor
@admin.register(Produccion)
class ProduccionAdmin(admin.ModelAdmin):
    form = ProduccionAdminForm

    list_display = ('producto', 'Litros_producido', 'fecha_produccion', 'turno', 'hora_registro', 'operador', 'anulado', 'usuario_anulacion', 'fecha_anulacion')
    list_filter = ('fecha_produccion', 'turno', 'anulado')
    search_fields = ('producto__nombre', 'operador__username')
    actions = ['anular_registros']

    def anular_registros(self, request, queryset):
        # Marcar los registros seleccionados como anulados
        queryset.update(anulado=True, usuario_anulacion=request.user, fecha_anulacion=timezone.now())
        self.message_user(request, "Los registros seleccionados han sido anulados correctamente.")
    anular_registros.short_description = "Anular registros seleccionados"

    def save_model(self, request, obj, form, change):
        if change and obj.anulado and not obj.usuario_anulacion:
            obj.usuario_anulacion = request.user
            obj.fecha_anulacion = timezone.now()
        super().save_model(request, obj, form, change)
