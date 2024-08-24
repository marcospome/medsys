from django import forms
from .models import Turno
from apps.socio.models import Paciente
from apps.base.models import Area
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TurnoForm(forms.ModelForm):
    medico = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Turno
        fields = ['fecha', 'horario', 'observacion', 'socio', 'usuario', 'estado', 'area']  # Agregamos 'estado' al conjunto de campos
        widgets = {
            'area': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'socio': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),  # Agregamos readonly para el campo de estado
        }

    def __init__(self, *args, **kwargs):

        medicos = kwargs.pop('medicos', None)
        super().__init__(*args, **kwargs)
        if medicos is not None:
            self.fields['usuario'].queryset = medicos
            self.fields['horario'].queryset = Turno.objects.none()
        # Agregar atributo 'min' para la fecha mínima
        if self.instance and self.instance.estado  in ['2', '3', '5', '1']:  # '5' Cancelado  ,'1' Atendido, '2' Ausente con aviso, '3' Ausente sin aviso'
            for field in self.fields:
                self.fields[field].disabled = True
        
        # Si el estado actual del turno no es 'Atendido', excluye 'Atendido' del campo estado
        if self.instance and self.instance.estado != '1':  # '1' Atendido
            exclude_choices = ['1']
            self.fields['estado'].choices = [(key, value) for key, value in self.fields['estado'].choices if key not in exclude_choices]


class FiltroTurnosForm(forms.Form):
    medico = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Medico'), required=False, label='Médico')
    socio = forms.ModelChoiceField(queryset=Paciente.objects.all(), required=False, label='Socio')
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False, label='Area')
    activo = forms.BooleanField(required=False, label='Activo')


        

