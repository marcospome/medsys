from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import HistorialClinico
from apps.turno.models import Turno  # Asegúrate de importar correctamente el modelo Turno
from .forms import HistorialClinicoForm

def crear_historial_clinico(request, turno_id):
    turno = get_object_or_404(Turno, pk=turno_id)

    if request.method == 'POST':
        form = HistorialClinicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.socio = turno.socio
            historial.usuario = request.user  # Usuario autenticado
            historial.save()

            # Actualizar el estado del turno a 'Atendido'
            turno.estado = '1'  # '1' representa 'Atendido' según tu modelo
            turno.save()

            return redirect('turnos_list')  # Redirigir a la lista de turnos
    else:
        form = HistorialClinicoForm()

    context = {
        'form': form,
        'turno': turno,
    }
    return render(request, 'historialclinico/crearhistorial.html', context)
