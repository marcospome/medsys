from django.urls import path
from . import views

urlpatterns = [
    # Otras URLs pueden estar aquí
    path('crear-historial-clinico/<int:turno_id>/', views.crear_historial_clinico, name='crear_historial_clinico'),
    path('editar-observacion-psiquiatrica/<int:historial_id>/', views.editar_observacion_psiquiatrica, name='editar_observacion_psiquiatrica'),

]
