# Generated by Django 5.0.3 on 2024-10-07 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historialesclinicos', '0014_rename_detalle_historialclinico_detalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialclinico',
            name='eliminado',
            field=models.BooleanField(default=0, verbose_name='Eliminado'),
        ),
    ]
