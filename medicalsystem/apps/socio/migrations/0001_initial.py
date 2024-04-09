# Generated by Django 5.0.3 on 2024-04-09 01:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=100, verbose_name='Domicilio')),
                ('numero', models.CharField(blank=True, default='S/N', max_length=10)),
                ('codigo_postal', models.CharField(blank=True, max_length=10, null=True)),
                ('localidad', models.CharField(max_length=100)),
                ('partido', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Domicilio',
                'verbose_name_plural': 'Registro de Domicilios',
            },
        ),
        migrations.CreateModel(
            name='Referente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellidos', models.CharField(blank=True, max_length=100)),
                ('nombres', models.CharField(blank=True, max_length=100)),
                ('alias', models.CharField(max_length=100)),
                ('parroquia', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Referente Parroquial',
                'verbose_name_plural': 'Registro de Referentes',
            },
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_de_telefono', models.CharField(max_length=20, verbose_name='Número de contacto')),
                ('numero_de_telefono2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número de contacto 2')),
            ],
            options={
                'verbose_name': 'Telefono',
                'verbose_name_plural': 'Registro de Telefonos',
            },
        ),
        migrations.CreateModel(
            name='TipoCertificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tipo', models.CharField(max_length=100, verbose_name='Tipo de certificado')),
                ('descripcion', models.CharField(max_length=50, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Tipo de certificado',
                'verbose_name_plural': 'Tipos de certificado',
            },
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('categoria', models.CharField(choices=[('0', 'Demanda Espontánea'), ('1', 'Socio'), ('3', 'Socio Afiliado')], default='0', max_length=1, verbose_name='Categoria')),
                ('condicion_de_solicitud', models.CharField(choices=[('0', 'Titular'), ('1', 'Familiar'), ('2', 'No Aplica')], default='0', max_length=1, verbose_name='Condición de solicitud')),
                ('dni', models.CharField(help_text="<span style='color: red;font-weight: bold; text-transform: uppercase;'>¡Ingresar sin caracteres especiales o espacios ( - , * , _, . )!</span>", max_length=8, unique=True, verbose_name='DNI')),
                ('dnititular', models.CharField(blank=True, help_text="<span style='color: red;font-weight: bold; text-transform: uppercase;'>¡Colocar unicamente si el TIPO DE AFILIACIÓN ES FAMILIAR!</span>", max_length=8, null=True, verbose_name='DNI del Titular')),
                ('cuit', models.CharField(blank=True, help_text="<span style='color: red;font-weight: bold; text-transform: uppercase;'>¡Ingresar sin caracteres especiales o espacios ( - , * , _ )!</span>", max_length=20, null=True, verbose_name='CUIT')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('fecha_de_nacimiento', models.DateField()),
                ('sex', models.CharField(choices=[('0', 'Masculino'), ('1', 'Femenino'), ('3', 'Otro')], default='0', max_length=1, verbose_name='Sexo')),
                ('casilla_de_mail', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator(message='Ingresa un correo válido')])),
                ('monotributo', models.CharField(choices=[('0', 'Categoria A'), ('1', 'Categoria B'), ('2', 'Categoria C'), ('3', 'Categoria D'), ('4', 'Otro'), ('5', 'No tiene')], default='0', max_length=1, verbose_name='Monotributo')),
                ('dni_foto_frente', models.FileField(blank=True, null=True, upload_to='dni/')),
                ('dni_foto_dorso', models.FileField(blank=True, null=True, upload_to='dni/')),
                ('credencial', models.AutoField(primary_key=True, serialize=False)),
                ('observaciones', models.TextField(blank=True)),
                ('credencial_entregada', models.BooleanField(default=False)),
                ('domicilio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='socio.domicilio')),
                ('responsable_de_carga', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('referente_parroquial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='socio.referente')),
                ('telefono', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='socio.telefono', verbose_name='Número de contacto')),
            ],
            options={
                'verbose_name': 'Socio',
                'verbose_name_plural': 'Registro de socios',
            },
        ),
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificado', models.FileField(upload_to='certificados/')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socio.paciente')),
                ('tipocertificado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socio.tipocertificado')),
            ],
            options={
                'verbose_name': 'Certificado',
                'verbose_name_plural': 'Registro de certificados',
            },
        ),
    ]
