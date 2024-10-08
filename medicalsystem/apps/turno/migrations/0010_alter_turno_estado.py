# Generated by Django 5.0.3 on 2024-06-12 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turno', '0009_turno_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='estado',
            field=models.CharField(choices=[('0', 'Pendiente de Confirmación'), ('1', 'Atendido'), ('2', 'Ausente con aviso'), ('3', 'Ausente sin aviso'), ('4', 'Confirmado'), ('5', 'Cancelado')], default='0', max_length=2, verbose_name='Estado del turno'),
        ),
    ]
