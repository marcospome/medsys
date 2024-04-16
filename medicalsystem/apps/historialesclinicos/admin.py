from django.contrib import admin
from django.utils.html import strip_tags
from .models import HistorialClinico

class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ('get_fecha_display', 'socio', 'usuario', 'observacion_plain')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Si el objeto no tiene clave primaria (es decir, es un nuevo registro)
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    # Formatea la fecha aaaa/mm/dd a dd/mm/aaaa para visualizarla de esta manera.
    def get_fecha_display(self, obj):
        return obj.fecha.strftime('%d %B %Y')  # Formato de fecha personalizado
    get_fecha_display.short_description = 'Fecha de carga'

    def observacion_plain(self, obj):
        return strip_tags(obj.observacion)
    observacion_plain.short_description = 'Observación'

    def observacion_view(self, obj):
        return self.observacion_plain(obj)
    observacion_view.short_description = 'Observación'

    def observacion_change(self, obj):
        return obj.observacion
    observacion_change.short_description = 'Observación'

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields = list(fields)
            # Reemplaza el campo observacion con observacion_plain
            fields[fields.index('observacion')] = 'observacion_plain'
        return fields

    # Añade el campo fecha a los campos a mostrar en la vista de detalle
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fields = list(fieldsets[0][1]['fields'])
            fields.insert(0, 'fecha')
            fieldsets[0][1]['fields'] = tuple(fields)
        return fieldsets

admin.site.register(HistorialClinico, HistorialClinicoAdmin)
