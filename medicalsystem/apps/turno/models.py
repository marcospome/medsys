from django.contrib.auth.models import User
from django.db import models
from apps.socio.models import Paciente
from django.core.exceptions import ValidationError

class Turno(models.Model):
    HORARIOS = (
        ('0', '8:00 - 9:00'),
        ('1', '9:00 - 10:00'),
        ('2', '10:00 - 11:00'),
        ('3', '11:00 - 12:00'),
        ('4', '12:00 - 13:00'),
        ('5', '13:00 - 14:00'),
        ('6', '14:00 - 15:00'),
        ('7', '15:00 - 16:00'),
        ('8', '16:00 - 17:00'),
        ('9', '17:00 - 18:00'),
        ('10', '18:00 - 19:00')
    )

    fecha = models.DateField(verbose_name='Fecha del turno')
    horario = models.CharField(max_length=2, choices=HORARIOS, default='0', verbose_name='Horario del turno')
    observacion = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True, verbose_name='¿Turno Activo?')
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='turnos_asignados', on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Médico asignado')
    responsable_de_carga = models.ForeignKey(User, related_name='turnos_responsable', on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return f'Turno de {self.socio} - {self.fecha} - {dict(self.HORARIOS)[self.horario]}'

    def clean(self):
        # Validar que no exista otro turno para la misma fecha, horario y médico
        if self.activo and Turno.objects.filter(fecha=self.fecha, horario=self.horario, usuario=self.usuario, activo=True).exists():
            raise ValidationError('Ya existe un turno activo para este médico en este horario y fecha.')

    def save(self, *args, **kwargs):
        # Validar si el turno está siendo creado o modificado
        if not self.pk or (self.pk and not Turno.objects.filter(pk=self.pk, activo=True).exists()):
            self.full_clean()  # Ejecutar la validación solo si el turno es nuevo o está inactivo
        super().save(*args, **kwargs)

    def cambiar_estado(self):
        self.activo = not self.activo
        self.save()

    class Meta:
        verbose_name_plural = 'Turnos'
