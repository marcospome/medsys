# views.py
from django.shortcuts import render, redirect,  get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TurnoForm
from .models import Turno
from apps.base.models import Area
from apps.socio.models import Paciente
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from functools import wraps
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from django.contrib.auth.decorators import login_required




def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "No tiene acceso a este módulo")
                return redirect('/admin/')
            if not hasattr(request.user, 'groups'):
                messages.error(request, "No tiene acceso a este módulo")
                return redirect('/admin/')
            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(role in user_groups for role in roles):
                messages.error(request, "No tiene acceso a este módulo")
                return redirect('/admin/')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# ---------------------------------------------------- ¡¡¡¡VISTA DE CREACIÓN DE TURNOS!!!! -----------------------------------------------------------------------------

class CrearTurnoView(LoginRequiredMixin, View):
    template_name = 'turno/crear_turno.html'
    form_class = TurnoForm

    @method_decorator(role_required(['Administrativo', 'Super Administrativo']))
    def get(self, request):
        areas = Area.objects.all()  # Obtiene todas las áreas
        area_id = request.GET.get('area')
        if area_id:
            try:
                area = Area.objects.get(id=area_id)
            except Area.DoesNotExist:
                area = None
        else:
            area = None
        
        medicos = self.get_medicos_por_area(area) if area else User.objects.none()
        form = self.form_class(initial={'area': area.id if area else None}, medicos=medicos)
        
        return render(request, self.template_name, {'form': form, 'areas': areas, 'selected_area': area})

    def post(self, request):
        area_id = request.POST.get('area')
        try:
            area = Area.objects.get(id=area_id)
        except Area.DoesNotExist:
            area = None
        
        medicos = self.get_medicos_por_area(area) if area else User.objects.none()
        form = self.form_class(request.POST, medicos=medicos)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.responsable_de_carga = request.user
            turno.area = area
            turno.save()
            return redirect('turnos_list')
        
        return render(request, self.template_name, {'form': form, 'areas': Area.objects.all(), 'selected_area': area})

    def get_medicos_por_area(self, area):
        return User.objects.filter(areas=area) if area else User.objects.none()
    
    def ajax_get_medicos(self, request):
        area_id = request.GET.get('area')
        try:
            area = Area.objects.get(id=area_id)
        except Area.DoesNotExist:
            return JsonResponse({'medicos': []})
        
        medicos = self.get_medicos_por_area(area)
        medicos_list = list(medicos.values_list('id', 'username'))  
        
        return JsonResponse({'medicos': medicos_list})


# ---------------------------------------------------------------------------------------------------------------------------------

class ListaTurnosView(LoginRequiredMixin, View):
    template_name = 'turno/lista_turnos.html'
    paginate_by = 5  # Número de turnos por página

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        areas = Area.objects.all()
        turnos = Turno.objects.all()

        # Filtrar turnos unicamente por los que tiene el medico.
        if user.groups.filter(name='Medico').exists() and user.groups.count() == 1: # Que sea medico y unicamente medico (si tiene más de un rol no valida.)
            turnos = turnos.filter(usuario=user)

        # Filtrar turnos si el usuario es médico, mostrando solo los confirmados
        if user.groups.filter(name='Medico').exists() and user.groups.count() == 1: # Que sea medico y unicamente medico (si tiene más de un rol no valida.)
            turnos = turnos.filter(usuario=user, estado='4') 


        # Ordenar por fecha
        orden = request.GET.get('orden', 'asc')
        if orden == 'desc':
            turnos = turnos.order_by('-fecha')
        else:
            turnos = turnos.order_by('fecha')

        # Filtrar por área
        area_id = request.GET.get('area', None)
        if area_id:
            turnos = turnos.filter(area__id=area_id)

        # Filtrar por médico
        medico_id = request.GET.get('medico', None)
        if medico_id:
            turnos = turnos.filter(usuario__id=medico_id)

        # Filtrar por socio
        socio_id = request.GET.get('socio', None)
        if socio_id:
            turnos = turnos.filter(socio__credencial=socio_id)

        # Filtrar por estado
        estado = request.GET.get('estado', None)
        if estado:
            turnos = turnos.filter(estado=estado)

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
            'areas': areas,
            'turnos': turnos_paginados,
            'orden': orden,
            'area_id': area_id,  
            'medico_id': medico_id,
            'socio_id': socio_id,
            'estado': estado,
            'turno_estados': Turno.ESTADOS,
            'medicos': medicos,
            'socios': socios,
            'page_obj': turnos_paginados,
            'is_medico': user.groups.filter(name='Medico').exists(),  # Levanta todos los usuarios con el grupo Medico.
            'is_administrativo': user.groups.filter(name='Administrativo').exists(),  # Levanta todos los usuarios con el grupo Administrativo.
            'is_superadmin': user.groups.filter(name='Super Administrativo').exists()  # Levanta todos los usuarios con el grupo Super Administrativo.
        }
        return render(request, self.template_name, context)



# --------------------------------------- LOGICA PARA FILTRAR ENTRE HORARIOS DISPONIBLES Y OCUPADOS ---------------------------------------------------------------------------


class ObtenerHorariosDisponiblesView(View):
    def get(self, request):
        try:
            medico_id = request.GET.get('medico_id')
            fecha = request.GET.get('fecha')
            
            if not medico_id or not fecha:
                return JsonResponse({'error': 'Invalid parameters'}, status=400)
            
            fecha = parse_date(fecha)
            
            if not fecha:
                return JsonResponse({'error': 'Invalid date format'}, status=400)
            
            # Filtrar turnos activos que no están cancelados
            horarios_ocupados = Turno.objects.filter(
                fecha=fecha, 
                usuario_id=medico_id, 
                activo=True
            ).exclude(estado='5').values_list('horario', flat=True)
            
            horarios_disponibles = [(horario, text) for horario, text in Turno.HORARIOS if horario not in horarios_ocupados]
            
            return JsonResponse({'horarios': horarios_disponibles})
        except Exception as e:
            # Registrar el error para más detalles
            print(f"Error: {e}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    

class ObtenerMedicosView(View):
    def get(self, request, *args, **kwargs):
        area_id = request.GET.get('area_id')
        medicos = User.objects.filter(areas__id=area_id) if area_id else User.objects.none()
        medicos_list = list(medicos.values_list('id', 'username'))  
        return JsonResponse({'medicos': medicos_list})


# ------------------------------------------------------------------------------------------------------------------------------------------------------------


class EditarTurnoView(LoginRequiredMixin, View):
    
    template_name = 'turno/editar_turno.html'
    form_class = TurnoForm

    @method_decorator(role_required(['Administrativo', 'Super Administrativo']))
    def get(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk)
        grupo_medico = Group.objects.get(name='Medico')
        medicos = grupo_medico.user_set.all()
        form = self.form_class(instance=turno, medicos=medicos)
        return render(request, self.template_name, {'form': form, 'turno': turno, 'estado_turno': turno.estado})

    def post(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk)
        grupo_medico = Group.objects.get(name='Medico')
        medicos = grupo_medico.user_set.all()
        form = self.form_class(request.POST, instance=turno, medicos=medicos)
        if form.is_valid():
            form.save()
            return redirect('turnos_list')  # Redirigir a la lista de turnos
        return render(request, self.template_name, {'form': form, 'turno': turno, 'estado_turno': turno.estado})
    




# ------------------------------------------------------------ EXPORTANCIÓN A EXCEL DE TURNOS -----------------------------------------------------------------------------


@login_required

def export_turnos_to_excel(request):
    # Obtener los filtros aplicados desde la request
    orden = request.GET.get('orden', 'asc')
    medico_id = request.GET.get('medico', None)
    socio_id = request.GET.get('socio', None)
    estado = request.GET.get('estado', None)
    area_id = request.GET.get('area', None)

    turnos = Turno.objects.all()

    if medico_id:
        turnos = turnos.filter(usuario__id=medico_id)
    if socio_id:
        turnos = turnos.filter(socio__credencial=socio_id)
    if estado:
        turnos = turnos.filter(estado=estado)
    if area_id:
        turnos = turnos.filter(area_id=area_id)

    if orden == 'desc':
        turnos = turnos.order_by('-fecha')
    else:
        turnos = turnos.order_by('fecha')

    # Crear un archivo de Excel en memoria
    wb = Workbook()
    ws = wb.active
    ws.title = "Turnos"

    # Escribir los encabezados
    ws.append(["Área", "Fecha", "Horario", "Paciente", "Responsable de Carga", "Médico Asignado", "Estado"])

    # Escribir los datos de los turnos
    for turno in turnos:
        ws.append([
            turno.area.nombre,
            turno.fecha.strftime("%Y-%m-%d"),
            turno.get_horario_display(),
            f"{turno.socio.apellidos} {turno.socio.nombres}, DNI: {turno.socio.dni}",
            f"{turno.responsable_de_carga.first_name} {turno.responsable_de_carga.last_name}",
            f"{turno.usuario.first_name} {turno.usuario.last_name}",
            turno.get_estado_display()
        ])

    # Preparar la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=turnos.xlsx'
    wb.save(response)
    return response




