# Generated by Django 5.0.3 on 2024-04-26 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0003_alter_paciente_options_alter_certificado_certificado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='certificado',
            field=models.FileField(blank=True, null=True, upload_to='certificados/'),
        ),
        migrations.AlterField(
            model_name='certificado',
            name='tipocertificado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socio.tipocertificado', verbose_name='Tipo de certificado'),
        ),
    ]
