
from django.urls import path
from .views import CrearTurnoView, ListaTurnosView, ObtenerHorariosDisponiblesView

urlpatterns = [
    path('crear-turno/', CrearTurnoView.as_view(), name='crear_turno'),
    path('lista-turnos/', ListaTurnosView.as_view(), name='turnos_list'),
    path('obtener-horarios/', ObtenerHorariosDisponiblesView.as_view(), name='obtener_horarios_disponibles'),

]
