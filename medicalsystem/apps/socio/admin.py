
# En tu_app/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import *
from .resources import PacienteResource

class CustomImportExportModelAdmin(ImportExportModelAdmin):
    def get_export_formats(self):
        """
        Limita los formatos de exportación solo a xlsx.
        """
        formats = (
            base_formats.XLS,
        )
        return [f for f in formats if f().can_export()]

    def has_import_permission(self, request):
        """
        Desactiva el botón de importación.
        """
        return False

class PacienteAdmin(CustomImportExportModelAdmin):
    list_display = (
        'categoria',
        'monotributo',
        'dni',
        'telefono',
        'nombres',
        'apellidos',
        'calcular_edad',
        'credencial',
        'responsable_de_carga',
    )

    resource_class = PacienteResource

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Si el objeto no tiene clave primaria (es decir, es un nuevo registro)
            obj.responsable_de_carga = request.user
        super().save_model(request, obj, form, change)

    def calcular_edad(self, obj):
        return obj.calcular_edad()
    calcular_edad.short_description = "Edad"
    calcular_edad.admin_order_field = '-fecha_de_nacimiento'
    

    def telefono_display(self, obj):
        return obj.telefono if obj.telefono else "N/A"

    telefono_display.short_description = "Teléfono"

    search_fields = ('dni',)
    
    list_filter = ['categoria', 'monotributo', 'credencial_entregada']


class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('calle', 'numero', 'localidad')

class ReferenteAdmin(admin.ModelAdmin):
    list_display = ('alias', 'nombres', 'apellidos', 'parroquia',)

class TelefonoAdmin(admin.ModelAdmin):
    list_display = ('numero_de_telefono',)

admin.site.register(Certificado)
admin.site.register(TipoCertificado)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Domicilio, DomicilioAdmin)
admin.site.register(Referente, ReferenteAdmin)
admin.site.register(Telefono, TelefonoAdmin)
