# Generated by Django 5.0.3 on 2024-04-19 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turno', '0003_alter_turno_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Turno',
        ),
    ]
