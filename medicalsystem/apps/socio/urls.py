
from django.urls import path
from .views import PacienteDetailView

urlpatterns = [
    path('detalle/<int:pk>/', PacienteDetailView.as_view(), name='detalle_paciente'),

]
