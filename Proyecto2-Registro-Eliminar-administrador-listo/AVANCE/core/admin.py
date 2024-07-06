from django.contrib import admin


from .models import Planta,Producto,Produccion

admin.site.register(Planta)
admin.site.register(Producto)

@admin.register(Produccion)
class ProduccionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'Litros_producido', 'fecha_produccion', 'turno', 'hora_registro', 'operador', 'anulado', 'usuario_anulacion', 'fecha_anulacion')
    list_filter = ('fecha_produccion', 'turno', 'anulado')
    search_fields = ('producto__nombre', 'operador__username')

    actions = ['anular_registros']

    def anular_registros(self, request, queryset):
        # Marcar los registros seleccionados como anulados
        queryset.update(anulado=True, usuario_anulacion=request.user, fecha_anulacion=timezone.now())
        self.message_user(request, "Los registros seleccionados han sido anulados correctamente.")

    anular_registros.short_description = "Anular registros seleccionados"
