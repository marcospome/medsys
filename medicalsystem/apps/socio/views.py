from django.views.generic import DetailView
from .models import Paciente
from apps.turno.models import Turno
from apps.base.models import Area
from apps.historialesclinicos.models import HistorialClinico
from django.contrib.auth.models import Group

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'socio/detalle_paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        areas = Area.objects.all()
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
        user = self.request.user

        # Definir roles por área
        roles_por_area = {
            'PS': 'Psiquiatría',
            'CG': 'Medico',
            'OD': 'Odontología',
            'OT': 'Medico'
        }

        # Filtrar historiales por área y verificar permisos
        historiales_filtrados = []
        for historial in HistorialClinico.objects.filter(socio=paciente):
            rol_requerido = roles_por_area.get(historial.area, 'Medico')
            if user.groups.filter(name=rol_requerido).exists():
                historiales_filtrados.append(historial)

        context['turnos'] = Turno.objects.filter(socio=paciente)
        context['historiales'] = historiales_filtrados
        return context
