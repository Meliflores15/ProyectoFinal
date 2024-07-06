from django import forms
from .models import Produccion

class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        fields = ['producto', 'Litros_producido', 'fecha_produccion', 'turno', 'hora_registro']
        widgets = {
            'fecha_produccion': forms.DateInput(attrs={'type': 'date'}),
            'hora_registro': forms.TimeInput(attrs={'type': 'time', 'step': 60}),
        }