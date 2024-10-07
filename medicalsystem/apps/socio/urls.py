
from django.urls import path
from .views import PacienteDetailView, generar_pdf

urlpatterns = [
    path('detalle/<int:pk>/', PacienteDetailView.as_view(), name='detalle_paciente'),
    path('generar_pdf/', generar_pdf, name='generar_pdf'),



]
