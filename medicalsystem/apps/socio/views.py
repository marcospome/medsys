from django.views.generic import DetailView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.socio.models import Paciente
from django.http import HttpResponse
from apps.turno.models import Turno
from apps.historialesclinicos.models import HistorialClinico
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from django.views import View



class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'socio/detalle_paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()

        # Filtrar los historiales clínicos del paciente según las áreas a las que pertenece el usuario
        user_areas = self.request.user.areas.all()
        historiales_filtrados = HistorialClinico.objects.filter(area__in=user_areas, socio=paciente, eliminado=False)

        # Verificar si hay historiales clínicos disponibles o acceso
        if not historiales_filtrados.exists():
            context['historiales_msg'] = "El paciente no posee historia clínica o no tiene acceso a visualizarla."
        else:
            context['historiales'] = historiales_filtrados

        # Pasar los turnos del paciente al contexto
        context['turnos'] = Turno.objects.filter(socio=paciente)

        # Verificar si el usuario pertenece al grupo "Super Administrativo"
        context['is_super_admin'] = self.request.user.groups.filter(name='Super Administrativo').exists()

        return context


def generar_pdf(request):
    if request.method == "POST":
        historial_ids = request.POST.getlist('historial_ids')

        # Obtener el primer historial para determinar el paciente
        primer_historial = HistorialClinico.objects.get(id=historial_ids[0])
        
        # Acceder al paciente a través del campo socio
        paciente = primer_historial.socio  # Cambié esto de paciente a socio

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="historial_medico_{paciente.nombres}_{paciente.apellidos}_{paciente.dni}.pdf"'

        # Crear un documento PDF
        buffer = response
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Crear el contenido del PDF
        elements = []

        # Título del PDF
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=1,  # Centrar
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        title = Paragraph(f"Historial Médico de {paciente.nombres} {paciente.apellidos} (DNI: {paciente.dni})", title_style)
        elements.append(title)

        elements.append(Spacer(1, 12))  # Espaciador

        # Línea de separación
        elements.append(Paragraph("<hr />", styles['Normal']))

        elements.append(Spacer(1, 12))  # Espaciador

        for historial_id in historial_ids:
            historial = HistorialClinico.objects.get(id=historial_id)
            
            # Encabezado del área
            area_style = ParagraphStyle(
                'Area',
                parent=styles['Heading2'],
                fontSize=18,
                textColor=colors.black,
                spaceAfter=6
            )
            elements.append(Paragraph(f"Área: {historial.area.nombre}", area_style))

            # Información del historial
            elements.append(Paragraph(f"<strong>Motivo de Consulta:</strong> {historial.motivo}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Fecha de Carga:</strong> {historial.fecha.strftime('%d-%m-%Y')}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Antecedentes Familiares:</strong> {historial.antecedentefamiliar or 'No disponibles'}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Enfermedad Actual:</strong> {historial.enfermedad or 'No disponible'}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Indicaciones:</strong> {historial.indicacion or 'No disponibles'}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Problema:</strong> {historial.problema or 'No disponible'}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Detalle:</strong> {historial.detalle or 'No disponible'}", styles['Normal']))
            elements.append(Paragraph(f"<strong>Médico Responsable:</strong> {historial.usuario.get_full_name() if historial.usuario else 'No disponible'}", styles['Normal']))
            elements.append(Spacer(1, 20))  # Espacio entre historiales

        # Generar el PDF
        doc.build(elements)
        return response
