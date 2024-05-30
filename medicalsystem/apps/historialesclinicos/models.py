from django.db import models
from apps.socio.models import Paciente
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Importa RichTextField desde ckeditor

# ------- Modelo historiales clinicos -------

class HistorialClinico(models.Model):

    motivo = models.CharField(verbose_name='Motivo de consulta', max_length=300)
    antecedentefamiliar = models.CharField(verbose_name='Antecedentes Familiares', max_length=300, blank=True)
    enfermedad = models.CharField(verbose_name='Enfermedad Actual', max_length=300, blank=True)
    indicacion = models.CharField(verbose_name='Indicacion', max_length=300, blank=True)
    problema = models.CharField(verbose_name='Problema', max_length=300, blank=True)
    Detalle = models.CharField(verbose_name='Problema', max_length=500, blank=True)
    fecha = models.DateField(verbose_name='Fecha de carga', auto_now_add=True) # Fecha en la que se carga el historial | se autoasigna como un getdate()
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE) # Socio/Paciente al cual corresponde el historial.
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Medico Responsable') # Usuario que cargo el historial, debe ser un medico o superadmin ya que solo ellos tienen permiso para cargar nuevos historiales.

# ------- Función para traer x campos del modelo historiales clinicos -------

    def __str__(self):  
        return f"{self.fecha}, {self.socio}, {self.usuario}, {self.motivo}"