from django.db import models
from apps.socio.models import Paciente
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Importa RichTextField desde ckeditor

# Create your models here.
class HistorialClinico(models.Model):
    
    fecha = models.DateField(verbose_name='Fecha de carga', auto_now_add=True, editable=False)
    observacion = RichTextField()
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Medico Responsable', editable=False)

    def __str__(self):  
        return f"{self.fecha}, {self.socio}, {self.usuario}"