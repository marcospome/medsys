# Generated by Django 5.0.3 on 2024-08-16 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('turno', '0014_merge_20240630_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.area'),
        ),
    ]
