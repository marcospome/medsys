from django.views.generic import DetailView
from .models import Paciente
from apps.turno.models import Turno
from apps.historialesclinicos.models import HistorialClinico

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'socio/detalle_paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        user = self.request.user
        context['turnos'] = Turno.objects.filter(socio=paciente)
        context['historiales'] = HistorialClinico.objects.filter(socio=paciente)
        context['is_medicops'] = user.groups.filter(name='Psiquiatría').exists()
        return context
