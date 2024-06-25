from django.contrib.auth.models import User
from django.db import models
from apps.socio.models import Paciente
from django.core.exceptions import ValidationError

class Turno(models.Model):
    HORARIOS = (
        ('0', '8:00 - 8:15'),
        ('1', '8:15 - 8:30'),
        ('2', '8:30 - 8:45'),
        ('3', '8:45 - 9:00'),
        ('4', '9:00 - 9:15'),
        ('5', '9:15 - 9:30'),
        ('6', '9:30 - 9:45'),
        ('7', '9:45 - 10:00'),
        ('8', '10:00 - 10:15'),
        ('9', '10:15 - 10:30'),
        ('10', '10:30 - 10:45'),
        ('11', '10:45 - 11:00'),
        ('12', '11:00 - 11:15'),
        ('13', '11:15 - 11:30'),
        ('14', '11:30 - 11:45'),
        ('15', '11:45 - 12:00'),
        ('16', '12:00 - 12:15'),
        ('17', '12:15 - 12:30'),
        ('18', '12:30 - 12:45'),
        ('19', '12:45 - 13:00'),
        ('20', '13:00 - 13:15'),
        ('21', '13:15 - 13:30'),
        ('22', '13:30 - 13:45'),
        ('23', '13:45 - 14:00'),
        ('24', '14:00 - 14:15'),
        ('25', '14:15 - 14:30'),
        ('26', '14:30 - 14:45'),
        ('27', '14:45 - 15:00'),
        ('28', '15:00 - 15:15'),
        ('29', '15:15 - 15:30'),
        ('30', '15:30 - 15:45'),
        ('31', '15:45 - 16:00'),
        ('32', '16:00 - 16:15'),
        ('33', '16:15 - 16:30'),
        ('34', '16:30 - 16:45'),
        ('35', '16:45 - 17:00'),
        ('36', '17:00 - 17:15'),
        ('37', '17:15 - 17:30'),
        ('38', '17:30 - 17:45'),
        ('39', '17:45 - 18:00'),
        ('40', '18:00 - 18:15'),
        ('41', '18:15 - 18:30'),
        ('42', '18:30 - 18:45'),
        ('43', '18:45 - 19:00')
    )

    ESTADOS = (
        ('0', 'Pendiente de Confirmación'),
        ('1', 'Atendido'),
        ('2', 'Ausente con aviso'),
        ('3', 'Ausente sin aviso'),
        ('4', 'Confirmado'),
        ('5', 'Cancelado')
    )

    AREAS = (
        ('OD', 'Odontología'),
        ('CG', 'Consulta General'),
        ('PS', 'Psiquiatría'),
        ('OT', 'Otros')
    )

    area = models.CharField(max_length=2, choices=AREAS, default='CG', verbose_name='Área')
    fecha = models.DateField(verbose_name='Fecha del turno')
    horario = models.CharField(max_length=2, choices=HORARIOS, default='0', verbose_name='Horario del turno')
    observacion = models.CharField(max_length=300, blank=True)
    activo = models.BooleanField(default=True, verbose_name='¿Turno Activo?')
    estado = models.CharField(max_length=2, choices=ESTADOS, default='0', verbose_name='Estado del turno')
    socio = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='turnos_asignados', on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Médico asignado')
    responsable_de_carga = models.ForeignKey(User, related_name='turnos_responsable', on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return f'Turno de {self.socio} - {self.fecha} - {dict(self.HORARIOS)[self.horario]}'
    
    def save(self, *args, **kwargs):
        if self.pk:
            previous = Turno.objects.get(pk=self.pk)
            if previous.estado == '5' and self.estado != '5':
                raise ValidationError("No se puede volver a habilitar un turno cancelado, favor de crear uno nuevo.")
        super(Turno, self).save(*args, **kwargs)



    class Meta:
        verbose_name_plural = 'Turnos'
