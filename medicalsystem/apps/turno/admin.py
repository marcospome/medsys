from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Turno
import datetime

class TurnoAdminForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'

    error_messages = {
        'horario': {
            'invalid_choice': _("Ya existe un turno activo para este médico en la misma fecha y hora. Por favor, seleccione otro horario, otra fecha o consulte con otro médico."),
        },
    }

    def clean_fecha(self):
        # Convertir la fecha al formato YYYY-MM-DD
        fecha = self.cleaned_data['fecha']
        return fecha.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        horario = cleaned_data.get("horario")
        medico = cleaned_data.get("usuario")

        if 'activo' in self.changed_data:  # Si se está editando y se cambia el estado activo/inactivo
            if not cleaned_data['activo']:  # Si se está cambiando a inactivo
                # No es necesario realizar la validación si se está cambiando a inactivo
                return cleaned_data

        # Verificar si al menos un turno con la misma fecha, hora y médico está activo
        if fecha and horario and medico:
            turnos_activos_existen = Turno.objects.filter(fecha=fecha, horario=horario, usuario=medico, activo=True).exists()
            if turnos_activos_existen:
                raise ValidationError(
                    self.error_messages['horario']['invalid_choice'],
                    code='invalid_choice',
                    params={'value': horario},
                )

        return cleaned_data

class TurnoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'horario', 'socio', 'usuario', 'responsable_de_carga', 'activo']
    form = TurnoAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'usuario':
            grupo_medico = Group.objects.get(name='Medico')
            kwargs['queryset'] = grupo_medico.user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'horario':
            medico_seleccionado = request.POST.get('usuario') or request.GET.get('usuario')
            if medico_seleccionado:
                fecha_seleccionada = request.POST.get('fecha') or request.GET.get('fecha')
                if fecha_seleccionada:
                    fecha_seleccionada = datetime.datetime.strptime(fecha_seleccionada, '%d/%m/%Y').strftime('%Y-%m-%d')
                    horarios_ocupados = Turno.objects.filter(fecha=fecha_seleccionada, usuario=medico_seleccionado).values_list('horario', flat=True)
                    horarios_disponibles = [choice[0] for choice in Turno.HORARIOS if choice[0] not in horarios_ocupados]
                    if '0' not in horarios_disponibles:
                        horarios_disponibles.append('0')
                    kwargs['choices'] = [(choice[0], choice[1]) for choice in Turno.HORARIOS if choice[0] in horarios_disponibles]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Medico').exists():
            return qs.filter(usuario=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not obj.responsable_de_carga:
            obj.responsable_de_carga = request.user
        obj.save()

admin.site.register(Turno, TurnoAdmin)
