from django.views.generic import DetailView
from .models import Paciente
from apps.turno.models import Turno
from apps.base.models import Area
from apps.historialesclinicos.models import HistorialClinico

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'socio/detalle_paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()

        # Filtrar los historiales clínicos del paciente según las áreas a las que pertenece el usuario
        user_areas = self.request.user.areas.all()
        historiales_filtrados = HistorialClinico.objects.filter(area__in=user_areas, socio=paciente)

        # Verificar si hay historiales clínicos disponibles o acceso
        if not historiales_filtrados.exists():
            context['historiales_msg'] = "El paciente no posee historia clínica o no tiene acceso a visualizarla."
        else:
            context['historiales'] = historiales_filtrados

        # Pasar los turnos del paciente al contexto
        turnos = Turno.objects.filter(socio=paciente)
        context['turnos'] = turnos

        return context
