from django.contrib.auth.models import User
from django.db import models
from apps.socio.models import Paciente
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

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
    activo = models.BooleanField(default=True, verbose_name='¿Turno Activo?')
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='turnos_asignados', on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Medico asignado')
    responsable_de_carga = models.ForeignKey(User, related_name='turnos_responsable', on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return f'Turno de {self.socio} - {self.fecha} - {dict(self.HORARIOS)[self.horario]}'

@receiver(pre_save, sender=Turno)
def asignar_responsable_de_carga(sender, instance, **kwargs):
    if not instance.responsable_de_carga:
        instance.responsable_de_carga = get_user_model().objects.get(id=instance.usuario.id)
