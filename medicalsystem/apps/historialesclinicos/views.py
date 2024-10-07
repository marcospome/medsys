from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages  # Importa el sistema de mensajes
from .models import HistorialClinico
from apps.turno.models import Turno  
from .forms import HistorialClinicoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden



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

            messages.success(request, 'Historial clínico creado con éxito.')  # Mensaje de éxito
            return redirect('turnos_list')  # Redirigir a la lista de turnos
        else:
            messages.error(request, 'Error al crear el historial clínico. Verifica los datos.')  # Mensaje de error
    else:
        form = HistorialClinicoForm()

    context = {
        'form': form,
        'turno': turno,    
    }
    return render(request, 'historialclinico/crearhistorial.html', context)


@login_required
# Método para eliminar un historial clínico
def eliminar_historial(request, historial_id):
    # Verificar si el usuario pertenece al grupo "Super Administrativo"
    if not request.user.groups.filter(name='Super Administrativo').exists():
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")  # Opcional: Mensaje de error

    # Obtén el historial clínico por su ID
    historial = get_object_or_404(HistorialClinico, id=historial_id)
    
    # Marcar el historial como eliminado
    historial.eliminado = True  
    historial.save()  # Guarda los cambios

    # Obtén el paciente relacionado con el historial
    paciente = historial.socio  # socio debería ser un objeto Paciente

    # Redirigir a la vista de detalle del paciente
    return redirect(request.META.get('HTTP_REFERER'))  # Refresca la página actual