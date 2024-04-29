import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = '__all__'

class TurnoAdmin(admin.ModelAdmin):
    form = TurnoForm
    list_display = ('fecha', 'horario', 'socio', 'usuario', 'activo', 'responsable_de_carga')
    list_filter = ('fecha', 'horario', 'activo', 'usuario')
    search_fields = ('fecha', 'socio__nombre', 'usuario__username')

    def save_model(self, request, obj, form, change):
        # Asignar el usuario autenticado como responsable de carga
        obj.responsable_de_carga = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "usuario":
            kwargs["queryset"] = User.objects.filter(groups__name='Medico')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        formfield = super().formfield_for_choice_field(db_field, request, **kwargs)
        if db_field.name == "horario" and request.POST.get('activo', None):  # Verificar si 'activo' está presente en la solicitud POST
            # Obtener la fecha seleccionada del formulario
            fecha_seleccionada = request.POST.get('fecha') or request.GET.get('fecha')
            if fecha_seleccionada:
                # Procesar la fecha al formato AAAA-MM-DD
                try:
                    fecha_formateada = datetime.datetime.strptime(fecha_seleccionada, '%d/%m/%Y').strftime('%Y-%m-%d')
                    # Obtener los horarios ocupados para la fecha seleccionada
                    horarios_ocupados = Turno.objects.filter(fecha=fecha_formateada, activo=True).values_list('horario', flat=True)
                    # Filtrar los horarios disponibles
                    formfield.choices = [(key, value) for key, value in Turno.HORARIOS if key not in horarios_ocupados]
                except ValueError:
                    pass
        return formfield
    



admin.site.register(Turno, TurnoAdmin)
