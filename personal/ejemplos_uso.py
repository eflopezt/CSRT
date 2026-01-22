"""
Ejemplo de uso de las mejoras implementadas.

Este archivo muestra cómo usar los nuevos servicios, validadores y decoradores
en vistas y operaciones del sistema.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
import logging

# Importar servicios
from personal.services import GerenciaService, RosterService, PersonalService

# Importar validadores
from personal.validators import PersonalValidator, RosterValidator, validar_archivo_excel

# Importar decoradores
from personal.decorators import handle_exceptions, handle_api_exceptions, log_access

# Importar modelos
from personal.models import Area, Roster, Personal

# Configurar loggers
logger = logging.getLogger('personal.business')
security_logger = logging.getLogger('personal.security')


# ============================================================================
# EJEMPLO 1: Vista con manejo robusto de excepciones y logging
# ============================================================================

@login_required
@handle_exceptions(default_redirect='gerencia_list')
@log_access('Creación de nueva área')
def crear_gerencia_mejorada(request):
    """
    Vista mejorada para crear gerencias con:
    - Manejo automático de excepciones
    - Logging de seguridad
    - Uso de servicios transaccionales
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        responsable_id = request.POST.get('responsable_id')
        descripcion = request.POST.get('descripcion', '')
        
        # Obtener responsable si existe
        responsable = None
        if responsable_id:
            responsable = get_object_or_404(Personal, pk=responsable_id)
        
        # Usar el servicio (maneja transacciones y validaciones)
        area = AreaService.crear_gerencia(
            nombre=nombre,
            responsable=responsable,
            descripcion=descripcion,
            usuario=request.user
        )
        
        # El decorador maneja cualquier error automáticamente
        messages.success(request, f'Área "{area.nombre}" creada exitosamente.')
        return redirect('gerencia_list')
    
    # Renderizar formulario
    personal_disponible = Personal.objects.filter(estado='Activo')
    return render(request, 'personal/gerencia_form.html', {
        'personal_disponible': personal_disponible
    })


# ============================================================================
# EJEMPLO 2: Importación con validación de archivo y transacciones
# ============================================================================

@login_required
@handle_exceptions(default_redirect='gerencia_list')
@log_access('Importación masiva de gerencias')
def importar_gerencias_mejorado(request):
    """
    Vista mejorada para importar gerencias con:
    - Validación de archivo antes de procesar
    - Transacciones atómicas
    - Manejo robusto de errores
    - Logging completo
    """
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        
        # Validar archivo antes de procesar
        validar_archivo_excel(archivo)
        
        # Usar el servicio (maneja transacciones)
        resultado = GerenciaService.importar_desde_excel(
            archivo=archivo,
            usuario=request.user
        )
        
        # Mostrar resultados
        if resultado['creados'] > 0:
            messages.success(request, f"✓ {resultado['creados']} gerencias creadas")
        
        if resultado['actualizados'] > 0:
            messages.info(request, f"ℹ {resultado['actualizados']} gerencias actualizadas")
        
        if resultado['errores']:
            for error in resultado['errores'][:5]:  # Mostrar solo 5 primeros
                messages.warning(request, error)
        
        return redirect('gerencia_list')
    
    return render(request, 'personal/import_form.html', {
        'titulo': 'Importar Gerencias'
    })


# ============================================================================
# EJEMPLO 3: API con manejo de excepciones JSON
# ============================================================================

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
@login_required
@handle_api_exceptions
def api_aprobar_roster(request, roster_id):
    """
    API endpoint para aprobar cambios en roster con:
    - Manejo automático de excepciones
    - Respuestas JSON estructuradas
    - Logging de seguridad
    """
    # Usar el servicio (maneja validaciones y auditoría)
    roster = RosterService.aprobar_cambio(
        roster_id=roster_id,
        usuario=request.user
    )
    
    # El decorador convierte cualquier error a JSON automáticamente
    return JsonResponse({
        'success': True,
        'mensaje': 'Cambio aprobado exitosamente',
        'roster': {
            'id': roster.id,
            'personal': roster.personal.apellidos_nombres,
            'fecha': roster.fecha.isoformat(),
            'codigo': roster.codigo,
            'estado': roster.estado
        }
    })


# ============================================================================
# EJEMPLO 4: Operación con validadores manuales
# ============================================================================

@login_required
@handle_exceptions(default_redirect='roster_list')
def actualizar_roster_manual(request, roster_id):
    """
    Vista que muestra uso manual de validadores.
    """
    roster = get_object_or_404(Roster, pk=roster_id)
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        observaciones = request.POST.get('observaciones', '')
        
        # Validar manualmente antes de guardar
        try:
            # Validar código
            codigo_validado = RosterValidator.validar_codigo(codigo)
            
            # Validar permisos de fecha
            RosterValidator.validar_fecha_edicion(roster.fecha, request.user)
            
            # Usar servicio para actualizar (transaccional)
            roster_actualizado = RosterService.actualizar_roster(
                roster_id=roster_id,
                codigo=codigo_validado,
                usuario=request.user,
                observaciones=observaciones
            )
            
            messages.success(request, 'Roster actualizado exitosamente.')
            return redirect('roster_list')
            
        except ValidationError as e:
            # Los errores se manejan automáticamente por el decorador
            # Pero también podemos capturarlos manualmente si necesitamos
            messages.error(request, str(e))
    
    return render(request, 'personal/roster_form.html', {
        'roster': roster
    })


# ============================================================================
# EJEMPLO 5: Logging manual en lógica de negocio
# ============================================================================

@login_required
@handle_exceptions(default_redirect='personal_list')
def validar_dni_personal(request):
    """
    Vista que muestra uso de logging manual.
    """
    if request.method == 'POST':
        nro_doc = request.POST.get('nro_doc')
        tipo_doc = request.POST.get('tipo_doc', 'DNI')
        
        try:
            # Validar documento
            PersonalValidator.validar_nro_doc(nro_doc, tipo_doc)
            
            # Log de éxito
            logger.info(
                f"Documento validado: {tipo_doc} {nro_doc} por "
                f"usuario {request.user.username}"
            )
            
            messages.success(request, 'Documento válido.')
            
        except ValidationError as e:
            # Log de error de validación
            logger.warning(
                f"Documento inválido: {tipo_doc} {nro_doc} - "
                f"Error: {str(e)} - Usuario: {request.user.username}"
            )
            messages.error(request, str(e))
    
    return render(request, 'personal/validar_dni.html')


# ============================================================================
# EJEMPLO 6: Operación compleja con múltiples transacciones
# ============================================================================

@login_required
@handle_exceptions(default_redirect='home')
@log_access('Operación compleja con múltiples cambios')
def operacion_compleja_ejemplo(request):
    """
    Ejemplo de operación que modifica múltiples entidades.
    Todo dentro de una transacción atómica.
    """
    if request.method == 'POST':
        with transaction.atomic():
            try:
                # Crear gerencia
                area = AreaService.crear_gerencia(
                    nombre="Nueva Área",
                    usuario=request.user
                )
                logger.info(f"Área creada: {gerencia.nombre}")
                
                # Crear personal
                personal_data = {
                    'nro_doc': '12345678',
                    'tipo_doc': 'DNI',
                    'apellidos_nombres': 'Juan Pérez',
                    'cargo': 'Analista',
                    'tipo_trab': 'Empleado',
                }
                personal = PersonalService.crear_personal(
                    datos=personal_data,
                    usuario=request.user
                )
                logger.info(f"Personal creado: {personal.apellidos_nombres}")
                
                # Si algo falla, todo se revierte automáticamente
                messages.success(
                    request,
                    'Operación completa exitosa. Área y personal creados.'
                )
                
            except ValidationError as e:
                # La transacción se revierte automáticamente
                logger.error(f"Error en operación compleja: {str(e)}")
                # El decorador maneja el error
                raise
        
        return redirect('home')
    
    return render(request, 'personal/operacion_compleja.html')


# ============================================================================
# EJEMPLO 7: Logging de seguridad para acciones críticas
# ============================================================================

@login_required
@handle_exceptions(default_redirect='home')
def eliminar_datos_criticos(request, objeto_id):
    """
    Vista que requiere logging de seguridad especial.
    """
    # Log de seguridad ANTES de la acción
    security_logger.warning(
        f"INTENTO DE ELIMINACIÓN - Usuario: {request.user.username}, "
        f"IP: {request.META.get('REMOTE_ADDR')}, "
        f"Objeto ID: {objeto_id}"
    )
    
    if not request.user.is_superuser:
        security_logger.error(
            f"ELIMINACIÓN DENEGADA - Usuario sin permisos: {request.user.username}"
        )
        messages.error(request, 'No tienes permisos para eliminar.')
        return redirect('home')
    
    # Realizar eliminación
    # ... código de eliminación ...
    
    # Log de seguridad DESPUÉS de la acción
    security_logger.warning(
        f"ELIMINACIÓN EXITOSA - Usuario: {request.user.username}, "
        f"Objeto ID: {objeto_id}"
    )
    
    messages.success(request, 'Objeto eliminado exitosamente.')
    return redirect('home')
