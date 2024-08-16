from django.db import models
from django.contrib.auth.models import User


# ------- Modelo área -------

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    verenturno = models.BooleanField(default=False)
# ------- Función para traer x campos del modelo área -------

    def __str__(self):  
        return f"{self.nombre}"
    

User.add_to_class('areas', models.ManyToManyField(Area, related_name="usuarios", blank=True))
