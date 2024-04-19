from django.db import models
from apps.socio.models import Paciente
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Importa RichTextField desde ckeditor

# ------- Modelo historiales clinicos -------

class HistorialClinico(models.Model):
    
    fecha = models.DateField(verbose_name='Fecha de carga', auto_now_add=True) # Fecha en la que se carga el historial | se autoasigna como un getdate()
    observacion = RichTextField() # Campo de texto estilo word para qué el medico pueda describir todo el detalle del paciente.
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE) # Socio/Paciente al cual corresponde el historial.
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Medico Responsable', editable=False) # Usuario que cargo el historial, debe ser un medico o superadmin ya que solo ellos tienen permiso para cargar nuevos historiales.

# ------- Función para traer x campos del modelo historiales clinicos -------

    def __str__(self):  
        return f"{self.fecha}, {self.socio}, {self.usuario}"