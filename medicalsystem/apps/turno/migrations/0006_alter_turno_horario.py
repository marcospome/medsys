# Generated by Django 5.0.3 on 2024-04-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turno', '0005_alter_turno_responsable_de_carga_alter_turno_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='horario',
            field=models.CharField(choices=[('0', '8:00 - 9:00'), ('1', '9:00 - 10:00'), ('2', '10:00 - 11:00'), ('3', '11:00 - 12:00'), ('4', '12:00 - 13:00'), ('5', '13:00 - 14:00'), ('6', '14:00 - 15:00'), ('7', '15:00 - 16:00'), ('8', '16:00 - 17:00'), ('9', '17:00 - 18:00')], default='0', max_length=1, verbose_name='Horario del turno'),
        ),
    ]
