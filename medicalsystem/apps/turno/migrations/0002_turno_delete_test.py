# Generated by Django 5.0.3 on 2024-04-11 03:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0001_initial'),
        ('turno', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(verbose_name='Fecha del turno')),
                ('horario', models.CharField(choices=[('0', '8:00 - 9:00'), ('1', '9:00 - 10:00'), ('3', '10:00 - 11:00'), ('4', '11:00 - 12:00'), ('5', '12:00 - 13:00'), ('6', '13:00 - 14:00'), ('7', '14:00 - 15:00'), ('8', '15:00 - 16:00'), ('9', '16:00 - 17:00'), ('10', '17:00 - 18:00')], default='0', max_length=2, verbose_name='Horario del turno')),
                ('observacion', models.CharField(blank=True, max_length=300)),
                ('activo', models.BooleanField(default=True, verbose_name='¿Turno Activo?')),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socio.paciente')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario asignado')),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
