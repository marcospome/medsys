from django import forms  # Importa el módulo de formularios de Django
from django.contrib import admin  # Importa el módulo de administración de Django
from django.contrib.auth.models import Group  # Importa el modelo de grupos de usuarios de Django
from django.core.exceptions import ValidationError  # Importa la excepción de validación de Django
from django.utils.translation import gettext_lazy as _  # Importa la función de traducción de Django
from .models import Turno  # Importa el modelo Turno desde el archivo models.py del mismo directorio
import datetime  # Importa el módulo datetime de Python estándar

# Define un formulario personalizado para el modelo Turno
class TurnoAdminForm(forms.ModelForm):
    class Meta:
        model = Turno  # Especifica el modelo asociado al formulario
        fields = '__all__'  # Define que se deben incluir todos los campos del modelo

    # Define mensajes de error personalizados
    error_messages = {
        'horario': {
            'invalid_choice': _("Ya existe un turno activo para este médico en la misma fecha y hora. Por favor, seleccione otro horario, otra fecha o consulte con otro médico."),
        },
    }

    # Método para limpiar y validar el campo 'fecha'
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        return fecha.strftime('%Y-%m-%d')  # Convierte la fecha al formato YYYY-MM-DD

    # Método para realizar validaciones personalizadas en todos los campos del formulario
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        horario = cleaned_data.get("horario")
        medico = cleaned_data.get("usuario")

        # Verifica si se está editando y se cambia el estado activo/inactivo
        if 'activo' in self.changed_data:
            # Si se está cambiando a inactivo, no es necesario realizar la validación
            if not cleaned_data['activo']:
                return cleaned_data

        # Verifica si hay un turno activo para el mismo médico en la misma fecha y hora
        if fecha and horario and medico:
            turnos_activos_existen = Turno.objects.filter(fecha=fecha, horario=horario, usuario=medico, activo=True).exists()
            if turnos_activos_existen:
                raise ValidationError(
                    self.error_messages['horario']['invalid_choice'],
                    code='invalid_choice',
                    params={'value': horario},
                )

        return cleaned_data

# Define la clase TurnoAdmin para personalizar la interfaz de administración del modelo Turno
class TurnoAdmin(admin.ModelAdmin):
    # Especifica los campos a mostrar en la lista de turnos en el panel de administración
    list_display = ['fecha', 'horario', 'socio', 'usuario', 'responsable_de_carga', 'activo']
    # Asocia el formulario personalizado al modelo Turno en el panel de administración
    form = TurnoAdminForm

    # Método para traer unicamente los usuarios con rol Medico en la lista de "Medico Asignado".
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'usuario':
            grupo_medico = Group.objects.get(name='Medico')
            kwargs['queryset'] = grupo_medico.user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Método para que limpie la lista de horarios y saque los no disponibles.
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

    # Método para que cada medico vea unicamente los turnos que tiene asignados a el mismo.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Medico').exists():
            return qs.filter(usuario=request.user)
        return qs

    # Método para guardar el turno con el usuario autenticado como responsable.
    def save_model(self, request, obj, form, change):
        if not obj.responsable_de_carga:
            obj.responsable_de_carga = request.user
        obj.save()

# Registra el modelo Turno y la clase TurnoAdmin en el panel de administración de Django
admin.site.register(Turno, TurnoAdmin)
