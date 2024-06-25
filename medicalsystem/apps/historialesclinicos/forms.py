from django import forms
from .models import HistorialClinico

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ['motivo', 'antecedentefamiliar', 'enfermedad', 'indicacion', 'problema', 'Detalle', 'observacionps']

class ObservacionPsiquiatricaForm(forms.ModelForm):
    observacionps = forms.CharField(label='Observación Psiquiátrica', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = HistorialClinico
        fields = ['observacionps']