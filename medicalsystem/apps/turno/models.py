from django.db import models

# Create your models here.
class Test(models.Model):
    Nombre = models.CharField(max_length=50)