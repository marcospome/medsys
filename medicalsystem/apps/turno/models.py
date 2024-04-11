from django.contrib.auth.models import User
from django.db import models
from apps.socio.models import Paciente

class Turno(models.Model):
    HORARIOS = (
        ('0', '8:00 - 9:00'),
        ('1', '9:00 - 10:00'),
        ('3', '10:00 - 11:00'),
        ('4', '11:00 - 12:00'),
        ('5', '12:00 - 13:00'),
        ('6', '13:00 - 14:00'),
        ('7', '14:00 - 15:00'),
        ('8', '15:00 - 16:00'),
        ('9', '16:00 - 17:00'),
        ('10', '17:00 - 18:00')
    )

    fecha = models.DateField(verbose_name='Fecha del turno')
    horario = models.CharField(max_length=2, choices=HORARIOS, default='0', verbose_name='Horario del turno')
    observacion = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True, verbose_name='¿Turno Activo?', null=False)
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuario asignado')
    
    def __str__(self):
        return f'Turno de {self.socio} - {self.fecha} - {dict(self.HORARIOS)[self.horario]}'
