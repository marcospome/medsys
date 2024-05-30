from django.contrib import admin
from django.utils.html import strip_tags, mark_safe
from .models import HistorialClinico

class HistorialClinicoAdmin(admin.ModelAdmin):
    # Lista de campos a mostrar en la lista de registros
    list_display = ('get_fecha_display', 'socio', 'usuario', 'motivo')
    list_filter = ['socio']


# ---------------------------- METODOS/LOGICA DEL ADMISTRADOR DE DJANGO PARA EL MODULO DE HISTORIALES CLINICOS ----------------------------
    def save_model(self, request, obj, form, change):
        # Asigna el usuario actual como el responsable del historial si es un registro nuevo, si se edita no cuenta de igual manera no se puede editar si no es superadmin.
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    # Formatea la fecha a formato personalizado para mostrarla en la lista de registros
    def get_fecha_display(self, obj):
        return obj.fecha.strftime('%d %B %Y')
    get_fecha_display.short_description = 'Fecha de carga'





    # Obtiene los campos que se mostrarán en el formulario
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            # Añade el campo 'usuario' si no está presente
            if 'usuario' not in fields:
                fields.append('usuario')
        return fields


    
    # ---------------------------- METODOS/LOGICA DEL ADMISTRADOR DE DJANGO PARA EL MODULO DE HISTORIALES CLINICOS ----------------------------


# Registra el modelo HistorialClinico junto con su administrador personalizado
admin.site.register(HistorialClinico, HistorialClinicoAdmin)
