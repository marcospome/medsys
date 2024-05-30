from django import forms
from .models import Turno
from apps.socio.models import Paciente
from datetime import datetime
from django.contrib.auth.models import User

class TurnoForm(forms.ModelForm):
    medico = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Turno
        fields = ['fecha', 'horario', 'observacion', 'socio', 'usuario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'socio': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        medicos = kwargs.pop('medicos', None)
        super().__init__(*args, **kwargs)
        if medicos is not None:
            self.fields['usuario'].queryset = medicos
            self.fields['horario'].queryset = Turno.objects.none()
        # Agregar atributo 'min' para la fecha mínima
        self.fields['fecha'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%d')

class FiltroTurnosForm(forms.Form):
    medico = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Medico'), required=False, label='Médico')
    socio = forms.ModelChoiceField(queryset=Paciente.objects.all(), required=False, label='Socio')
    activo = forms.BooleanField(required=False, label='Activo')
