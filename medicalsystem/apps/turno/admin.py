from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Turno

class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%d/%m/%Y'

class TurnoAdminForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'
        widgets = {
            'fecha': DateInput(),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        horario = cleaned_data.get("horario")
        medico = cleaned_data.get("usuario")
        if fecha and horario and medico:
            turno_existente = Turno.objects.filter(fecha=fecha, horario=horario, usuario=medico).exists()
            if turno_existente:
                raise ValidationError(_("El horario seleccionado ya está reservado por otro médico en la misma fecha. Por favor, seleccione otro horario, otra fecha o consulte con otro médico."), code='invalid')
        return cleaned_data

class TurnoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'horario', 'socio', 'usuario', 'responsable_de_carga']
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
        if not obj.responsable_de_carga:  # Si no se ha asignado un responsable de carga
            obj.responsable_de_carga = request.user  # Asigna el usuario autenticado
        obj.save()

admin.site.register(Turno, TurnoAdmin)
