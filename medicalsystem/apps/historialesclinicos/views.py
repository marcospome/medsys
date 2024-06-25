from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import HistorialClinico
from .forms import ObservacionPsiquiatricaForm

from django.contrib.auth.models import User, Group

from apps.turno.models import Turno  # Asegúrate de importar correctamente el modelo Turno
from .forms import HistorialClinicoForm

def crear_historial_clinico(request, turno_id):
    turno = get_object_or_404(Turno, pk=turno_id)
    user = request.user

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
        'is_medicops': user.groups.filter(name='Psiquiatría').exists(),
    }
    return render(request, 'historialclinico/crearhistorial.html', context)


def editar_observacion_psiquiatrica(request, historial_id):
    historial = get_object_or_404(HistorialClinico, pk=historial_id)
    
    if request.method == 'POST':
        form = ObservacionPsiquiatricaForm(request.POST, instance=historial)
        if form.is_valid():
            form.save()
            return redirect('turnos_list')  # Cambia 'turnos_list' por el nombre de tu URL para redirigir
    else:
        form = ObservacionPsiquiatricaForm(instance=historial)
    
    context = {
        'form': form,
        'historial': historial,
    }
    return render(request, 'historialclinico/editar_observacion_psiquiatrica.html', context)