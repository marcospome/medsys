# En tu_app/resources.py
from import_export import resources
from import_export.fields import Field
from .models import Paciente

class PacienteResource(resources.ModelResource):
    dni = Field(column_name='DNI', attribute='dni')
    nombres = Field(column_name='Nombre/s', attribute='nombres')
    apellidos = Field(column_name='Apellido/s', attribute='apellidos')
    numero_de_contacto = Field(column_name='Número de contacto', attribute='telefono__numero_de_telefono')
    categoria_display = Field(column_name='Categoría', attribute='get_categoria_display')
    monotributo_display = Field(column_name='Monotributo', attribute='get_monotributo_display')
    credencial = Field(column_name='Número de credencial', attribute='credencial')

    class Meta:
        model = Paciente
        fields = (
            'categoria_display',
            'dni',
            'nombres',
            'apellidos',
            'numero_de_contacto',
            'monotributo_display',
            'credencial',
        )

    def get_export_order(self, *args, **kwargs):
        return self._meta.fields
