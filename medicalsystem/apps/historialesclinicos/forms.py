from django import forms
from .models import HistorialClinico

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['motivo', 'antecedentefamiliar', 'enfermedad', 'indicacion', 'problema', 'Detalle', 'area']

        widgets = {
            'area': forms.Select(attrs={'class': 'form-control'}),
        }


