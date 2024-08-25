from django.db import models
from apps.socio.models import Paciente
from apps.base.models import Area
from django.contrib.auth.models import User

# ------- Modelo historiales clinicos -------

class HistorialClinico(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE) # Area la cual corresponde el historial
    motivo = models.CharField(verbose_name='Motivo de consulta', max_length=500)
    antecedentefamiliar = models.CharField(verbose_name='Antecedentes Familiares', max_length=10000, blank=True, null=True)
    enfermedad = models.CharField(verbose_name='Enfermedad Actual', max_length=10000, blank=True, null=True)
    indicacion = models.CharField(verbose_name='Indicacion', max_length=10000, blank=True, null=True)
    problema = models.CharField(verbose_name='Problema', max_length=10000, blank=True, null=True)
    detalle = models.CharField(verbose_name='Detalle', max_length=10000, blank=True, null=True)
    fecha = models.DateField(verbose_name='Fecha de carga', auto_now_add=True) # Fecha en la que se carga el historial | se autoasigna como un getdate()
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE) # Socio/Paciente al cual corresponde el historial.
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Medico Responsable') # Usuario que cargo el historial, debe ser un medico o superadmin ya que solo ellos tienen permiso para cargar nuevos historiales.

# ------- Función para traer x campos del modelo historiales clinicos -------

    def __str__(self):  
        return f"{self.fecha}, {self.socio}, {self.usuario}, {self.motivo}"