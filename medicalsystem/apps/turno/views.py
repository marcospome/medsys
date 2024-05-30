# views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TurnoForm
from .models import Turno
from apps.socio.models import Paciente
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.dateparse import parse_date

class CrearTurnoView(LoginRequiredMixin, View):
    template_name = 'turno/crear_turno.html'
    form_class = TurnoForm

    def get(self, request):
        grupo_medico = Group.objects.get(name='Medico')
        medicos = User.objects.filter(groups=grupo_medico)
        form = self.form_class(medicos=medicos)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        grupo_medico = Group.objects.get(name='Medico')
        medicos = User.objects.filter(groups=grupo_medico)
        form = self.form_class(request.POST, medicos=medicos)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.responsable_de_carga = request.user
            turno.save()
            return redirect('turnos_list')  # Redirigir a la lista de turnos
        return render(request, self.template_name, {'form': form})



class ListaTurnosView(LoginRequiredMixin, View):
    template_name = 'turno/lista_turnos.html'
    paginate_by = 4  # Número de turnos por página

    def get(self, request):
        turnos = Turno.objects.all()

        # Ordenar por fecha
        orden = request.GET.get('orden', 'asc')
        if orden == 'desc':
            turnos = turnos.order_by('-fecha')
        else:
            turnos = turnos.order_by('fecha')

        # Filtrar por médico
        medico_id = request.GET.get('medico', None)
        if medico_id:
            turnos = turnos.filter(usuario__id=medico_id)

        # Filtrar por socio
        socio_id = request.GET.get('socio', None)
        if socio_id:
            turnos = turnos.filter(socio__credencial=socio_id)

        # Filtrar por activo
        activo = request.GET.get('activo', None)
        if activo == 'true':
            turnos = turnos.filter(activo=True)
        elif activo == 'false':
            turnos = turnos.filter(activo=False)

        # Obtener lista de médicos y socios
        grupo_medico = Group.objects.get(name='Medico')
        medicos = User.objects.filter(groups=grupo_medico)
        socios = Paciente.objects.all()  # Obtener todos los pacientes para el formulario

        # Paginar los resultados
        paginator = Paginator(turnos, self.paginate_by)
        page = request.GET.get('page')
        try:
            turnos_paginados = paginator.page(page)
        except PageNotAnInteger:
            # Si la página no es un entero, mostrar la primera página
            turnos_paginados = paginator.page(1)
        except EmptyPage:
            # Si la página está fuera de rango (ej. 9999), mostrar la última página de resultados
            turnos_paginados = paginator.page(paginator.num_pages)

        context = {
            'turnos': turnos_paginados,
            'orden': orden,
            'medicos': medicos,
            'socios': socios,
        }
        return render(request, self.template_name, context)





class ObtenerHorariosDisponiblesView(LoginRequiredMixin, View):
    def get(self, request):
        medico_id = request.GET.get('medico_id')
        fecha = request.GET.get('fecha')
        
        if not medico_id or not fecha:
            return JsonResponse({'error': 'Invalid parameters'}, status=400)
        
        fecha = parse_date(fecha)
        horarios_ocupados = Turno.objects.filter(fecha=fecha, usuario_id=medico_id, activo=True).values_list('horario', flat=True)
        horarios_disponibles = [(horario, text) for horario, text in Turno.HORARIOS if horario not in horarios_ocupados]
        
        return JsonResponse({'horarios': horarios_disponibles})