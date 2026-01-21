"""
Vistas para el módulo personal.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal, InvalidOperation
import pandas as pd
from datetime import datetime, timedelta
from calendar import monthrange
from collections import defaultdict
import json

from .models import Gerencia, Area, Personal, Roster, RosterAudit
from .forms import GerenciaForm, AreaForm, PersonalForm, RosterForm, ImportExcelForm
from .permissions import (
    filtrar_gerencias, filtrar_areas, filtrar_personal,
    puede_editar_personal, get_context_usuario, es_responsable_gerencia
)


@login_required
def home(request):
    """Vista principal del sistema."""
    # Aplicar filtros según usuario
    gerencias_filtradas = filtrar_gerencias(request.user)
    areas_filtradas = filtrar_areas(request.user)
    personal_filtrado = filtrar_personal(request.user)
    
    context = {
        'total_gerencias': gerencias_filtradas.filter(activa=True).count(),
        'total_areas': areas_filtradas.filter(activa=True).count(),
        'total_personal': personal_filtrado.filter(estado='Activo').count(),
        'total_roster_hoy': Roster.objects.filter(
            fecha=datetime.now().date(),
            personal__in=personal_filtrado
        ).count(),
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'home.html', context)


def logout_view(request):
    """Vista personalizada de logout que acepta GET y POST."""
    auth_logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')


# ================== GERENCIAS ==================

@login_required
def gerencia_list(request):
    """Lista de gerencias."""
    # Aplicar filtros según usuario
    gerencias = filtrar_gerencias(request.user).annotate(
        total_areas=Count('areas'),
    ).order_by('nombre')
    
    # Filtros
    buscar = request.GET.get('buscar', '')
    if buscar:
        gerencias = gerencias.filter(
            Q(nombre__icontains=buscar) |
            Q(responsable__apellidos_nombres__icontains=buscar)
        )
    
    context = {
        'gerencias': gerencias,
        'buscar': buscar
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/gerencia_list.html', context)


@login_required
def gerencia_create(request):
    """Crear nueva gerencia."""
    if request.method == 'POST':
        form = GerenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gerencia creada exitosamente.')
            return redirect('gerencia_list')
    else:
        form = GerenciaForm()
    
    return render(request, 'personal/gerencia_form.html', {'form': form})


@login_required
def gerencia_update(request, pk):
    """Actualizar gerencia."""
    gerencia = get_object_or_404(Gerencia, pk=pk)
    
    if request.method == 'POST':
        form = GerenciaForm(request.POST, instance=gerencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gerencia actualizada exitosamente.')
            return redirect('gerencia_list')
    else:
        form = GerenciaForm(instance=gerencia)
    
    return render(request, 'personal/gerencia_form.html', {
        'form': form,
        'gerencia': gerencia
    })


# ================== ÁREAS ==================

@login_required
def area_list(request):
    """Lista de áreas."""
    # Aplicar filtros según usuario
    areas = filtrar_areas(request.user).select_related('gerencia').annotate(
        total_personal=Count('personal_asignado')
    ).order_by('gerencia__nombre', 'nombre')
    
    # Filtros
    gerencia_id = request.GET.get('gerencia', '')
    buscar = request.GET.get('buscar', '')
    
    if gerencia_id:
        areas = areas.filter(gerencia_id=gerencia_id)
    if buscar:
        areas = areas.filter(nombre__icontains=buscar)
    
    gerencias = Gerencia.objects.filter(activa=True)
    
    return render(request, 'personal/area_list.html', {
        'areas': areas,
        'gerencias': gerencias,
        'buscar': buscar,
        'gerencia_id': gerencia_id
    })


@login_required
def area_create(request):
    """Crear nueva área."""
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área creada exitosamente.')
            return redirect('area_list')
    else:
        form = AreaForm()
    
    return render(request, 'personal/area_form.html', {'form': form})


@login_required
def area_update(request, pk):
    """Actualizar área."""
    area = get_object_or_404(Area, pk=pk)
    
    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área actualizada exitosamente.')
            return redirect('area_list')
    else:
        form = AreaForm(instance=area)
    
    return render(request, 'personal/area_form.html', {
        'form': form,
        'area': area
    })


# ================== PERSONAL ==================

@login_required
def personal_list(request):
    """Lista de personal."""
    # Aplicar filtros según usuario
    personal = filtrar_personal(request.user).select_related('area', 'area__gerencia').order_by('apellidos_nombres')
    
    # Filtros
    estado = request.GET.get('estado', '')
    area_id = request.GET.get('area', '')
    buscar = request.GET.get('buscar', '')
    
    if estado:
        personal = personal.filter(estado=estado)
    if area_id:
        personal = personal.filter(area_id=area_id)
    if buscar:
        personal = personal.filter(
            Q(apellidos_nombres__icontains=buscar) |
            Q(nro_doc__icontains=buscar) |
            Q(cargo__icontains=buscar)
        )
    
    # Paginación
    paginator = Paginator(personal, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    areas = Area.objects.filter(activa=True).select_related('gerencia')
    
    return render(request, 'personal/personal_list.html', {
        'page_obj': page_obj,
        'areas': areas,
        'estado': estado,
        'area_id': area_id,
        'buscar': buscar
    })


@login_required
def personal_create(request):
    """Crear nuevo personal."""
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal creado exitosamente.')
            return redirect('personal_list')
    else:
        form = PersonalForm()
    
    return render(request, 'personal/personal_form.html', {'form': form})


@login_required
def personal_update(request, pk):
    """Actualizar personal."""
    # Verificar que el personal esté dentro del alcance del usuario
    personal = get_object_or_404(filtrar_personal(request.user), pk=pk)
    
    # Verificar permisos específicos
    if not puede_editar_personal(request.user, personal):
        messages.error(request, 'No tienes permisos para editar este personal.')
        return redirect('personal_list')
    
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal)
        if form.is_valid():
            # Si es responsable, validar que el área pertenezca a su gerencia
            if es_responsable_gerencia(request.user) and not request.user.is_superuser:
                nueva_area = form.cleaned_data.get('area')
                if nueva_area and nueva_area not in filtrar_areas(request.user):
                    messages.error(request, 'No puedes asignar personal a áreas fuera de tu gerencia.')
                    return render(request, 'personal/personal_form.html', {
                        'form': form,
                        'personal': personal
                    })
            
            form.save()
            messages.success(request, 'Personal actualizado exitosamente.')
            return redirect('personal_list')
    else:
        form = PersonalForm(instance=personal)
        # Si es responsable, limitar opciones de área
        if es_responsable_gerencia(request.user) and not request.user.is_superuser:
            form.fields['area'].queryset = filtrar_areas(request.user)
    
    context = {
        'form': form,
        'personal': personal
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/personal_form.html', context)


@login_required
def personal_detail(request, pk):
    """Detalle de personal."""
    personal = get_object_or_404(
        filtrar_personal(request.user).select_related('area', 'area__gerencia'),
        pk=pk
    )
    
    # Últimos registros de roster
    roster_reciente = Roster.objects.filter(personal=personal).order_by('-fecha')[:10]
    
    context = {
        'personal': personal,
        'roster_reciente': roster_reciente
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/personal_detail.html', context)


# ================== ROSTER ==================

@login_required
def roster_list(request):
    """Lista de registros de roster."""
    rosters = Roster.objects.select_related('personal', 'personal__area').all()
    
    # Filtros
    buscar = request.GET.get('buscar', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    if buscar:
        rosters = rosters.filter(
            Q(personal__nro_doc__icontains=buscar) |
            Q(personal__apellidos_nombres__icontains=buscar) |
            Q(codigo__icontains=buscar)
        )
    
    if fecha_desde:
        rosters = rosters.filter(fecha__gte=fecha_desde)
    
    if fecha_hasta:
        rosters = rosters.filter(fecha__lte=fecha_hasta)
    
    rosters = rosters.order_by('-fecha', 'personal__apellidos_nombres')
    
    # Paginación
    paginator = Paginator(rosters, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'personal/roster_list.html', {
        'page_obj': page_obj,
        'buscar': buscar,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    })


@login_required
def roster_matricial(request):
    """
    Vista matricial del roster: filas=personal, columnas=días del mes.
    Incluye columna de días libres ganados y días trabajados calculados.
    """
    # Obtener mes y año de los parámetros o usar el actual
    hoy = datetime.now().date()
    mes = int(request.GET.get('mes', hoy.month))
    anio = int(request.GET.get('anio', hoy.year))
    
    # Filtros adicionales
    area_id = request.GET.get('area', '')
    buscar = request.GET.get('buscar', '')
    
    # Calcular primer y último día del mes
    primer_dia = datetime(anio, mes, 1).date()
    ultimo_dia = datetime(anio, mes, monthrange(anio, mes)[1]).date()
    
    # Generar lista de fechas del mes
    fechas_mes = []
    fecha_actual = primer_dia
    while fecha_actual <= ultimo_dia:
        fechas_mes.append(fecha_actual)
        fecha_actual += timedelta(days=1)
    
    # Obtener personal activo con filtros según usuario
    personal_qs = filtrar_personal(request.user).filter(estado='Activo').select_related('area', 'area__gerencia')
    
    if area_id:
        personal_qs = personal_qs.filter(area_id=area_id)
    
    if buscar:
        personal_qs = personal_qs.filter(
            Q(nro_doc__icontains=buscar) |
            Q(apellidos_nombres__icontains=buscar)
        )
    
    personal_qs = personal_qs.order_by('apellidos_nombres')
    
    # Obtener todos los registros de roster del mes
    rosters = Roster.objects.filter(
        fecha__gte=primer_dia,
        fecha__lte=ultimo_dia,
        personal__in=personal_qs
    ).select_related('personal')
    
    # Organizar roster por personal y fecha
    roster_dict = defaultdict(dict)
    for r in rosters:
        roster_dict[r.personal_id][r.fecha] = r.codigo
    
    # Construir datos para la tabla
    tabla_datos = []
    for persona in personal_qs:
        # Obtener códigos del mes con sus fechas
        codigos_mes = []
        for fecha in fechas_mes:
            codigo = roster_dict[persona.id].get(fecha, '')
            codigos_mes.append({
                'fecha': fecha,
                'codigo': codigo
            })
        
        # Calcular días libres ganados del mes usando el régimen de turno
        count_t = sum(1 for item in codigos_mes if item['codigo'] == 'T')
        count_tr = sum(1 for item in codigos_mes if item['codigo'] == 'TR')
        count_dl = sum(1 for item in codigos_mes if item['codigo'] == 'DL')
        
        # Calcular factor para T según régimen de turno de la persona
        factor_t = 3  # Por defecto 21x7 -> 21/7 = 3
        if persona.regimen_turno:
            try:
                partes = persona.regimen_turno.strip().split('x')
                if len(partes) == 2:
                    dias_trabajo = int(partes[0])
                    dias_descanso = int(partes[1])
                    if dias_descanso > 0:
                        factor_t = dias_trabajo / dias_descanso
            except (ValueError, ZeroDivisionError):
                pass
        
        # TR siempre es 5x2
        factor_tr = 5.0 / 2.0  # 2.5 días TR por cada día libre
        
        # Calcular días libres ganados en el mes (con decimales)
        dias_libres_ganados_mes = round(count_t / factor_t + count_tr / factor_tr)
        
        # Calcular días libres pendientes totales
        dias_libres_ganados_total = persona.dias_libres_ganados
        dias_dl_usados_total = persona.calcular_dias_dl_usados()
        dias_libres_pendientes_total = float(persona.dias_libres_corte_2025) + dias_libres_ganados_total - dias_dl_usados_total
        
        fila = {
            'personal': persona,
            'dias_libres_corte_2025': persona.dias_libres_corte_2025,
            'dias_libres_ganados': dias_libres_ganados_total,
            'dias_libres_pendientes': dias_libres_pendientes_total,
            'count_t': count_t,
            'count_tr': count_tr,
            'count_dl': count_dl,
            'codigos': codigos_mes
        }
        tabla_datos.append(fila)
    
    # Obtener todas las áreas para el filtro
    areas = Area.objects.filter(activa=True).select_related('gerencia').order_by('gerencia__nombre', 'nombre')
    
    # Lista de meses para el selector
    meses = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]
    
    # Lista de años (últimos 3 y próximos 2)
    anios = list(range(hoy.year - 3, hoy.year + 3))
    
    context = {
        'tabla_datos': tabla_datos,
        'fechas_mes': fechas_mes,
        'mes': mes,
        'anio': anio,
        'mes_nombre': dict(meses)[mes],
        'meses': meses,
        'anios': anios,
        'areas': areas,
        'area_id': area_id,
        'buscar': buscar,
    }
    
    return render(request, 'personal/roster_matricial.html', context)


@login_required
def roster_create(request):
    """Crear nuevo registro de roster."""
    if request.method == 'POST':
        form = RosterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de roster creado exitosamente.')
            return redirect('roster_list')
    else:
        form = RosterForm()
    
    return render(request, 'personal/roster_form.html', {'form': form})


@login_required
def roster_update(request, pk):
    """Actualizar registro de roster."""
    roster = get_object_or_404(Roster, pk=pk)
    
    if request.method == 'POST':
        form = RosterForm(request.POST, instance=roster)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de roster actualizado exitosamente.')
            return redirect('roster_list')
    else:
        form = RosterForm(instance=roster)
    
    return render(request, 'personal/roster_form.html', {
        'form': form,
        'roster': roster
    })


# ================== IMPORT/EXPORT ==================

# Importar utilidades de Excel
from .excel_utils import (
    crear_plantilla_personal, crear_plantilla_gerencias,
    crear_plantilla_areas, crear_plantilla_roster
)

# ===== GERENCIAS =====

@login_required
def gerencia_export(request):
    """Exportar gerencias a Excel con plantilla y catálogos."""
    gerencias = filtrar_gerencias(request.user)
    
    # Crear plantilla con datos actuales
    excel_file = crear_plantilla_gerencias(gerencias)
    
    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=gerencias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return response


@login_required
def gerencia_import(request):
    """Importar gerencias desde Excel."""
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                df = pd.read_excel(archivo, sheet_name='Gerencias')
                
                # Validar columnas
                columnas_requeridas = ['Nombre']
                if not all(col in df.columns for col in columnas_requeridas):
                    messages.error(request, 'El archivo debe contener al menos la columna: Nombre')
                    return redirect('gerencia_import')
                
                creados = 0
                actualizados = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        nombre = str(row['Nombre']).strip()
                        if not nombre or nombre == 'nan':
                            continue
                        
                        # Buscar responsable si se proporciona DNI
                        responsable = None
                        if 'Responsable_DNI' in row and pd.notna(row['Responsable_DNI']):
                            try:
                                responsable = Personal.objects.get(nro_doc=str(row['Responsable_DNI']).strip())
                            except Personal.DoesNotExist:
                                errores.append(f"Fila {idx + 2}: Responsable con DNI {row['Responsable_DNI']} no encontrado")
                        
                        # Determinar si está activa
                        activa = True
                        if 'Activa' in row and pd.notna(row['Activa']):
                            activa = str(row['Activa']).strip().lower() in ['sí', 'si', 'yes', '1', 'true']
                        
                        # Crear o actualizar
                        gerencia, created = Gerencia.objects.update_or_create(
                            nombre=nombre,
                            defaults={
                                'responsable': responsable,
                                'descripcion': row.get('Descripcion', '') if pd.notna(row.get('Descripcion')) else '',
                                'activa': activa,
                            }
                        )
                        
                        if created:
                            creados += 1
                        else:
                            actualizados += 1
                    
                    except Exception as e:
                        errores.append(f"Fila {idx + 2}: {str(e)}")
                
                if creados > 0:
                    messages.success(request, f'✓ {creados} gerencias creadas')
                if actualizados > 0:
                    messages.info(request, f'ℹ {actualizados} gerencias actualizadas')
                if errores:
                    for error in errores[:10]:
                        messages.warning(request, error)
                
                return redirect('gerencia_list')
            
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
                return redirect('gerencia_import')
    else:
        form = ImportExcelForm()
    
    # Si se solicita plantilla vacía, generarla y descargar
    if request.GET.get('plantilla') == 'vacia':
        excel_file = crear_plantilla_gerencias(None)
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=plantilla_gerencias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return response
    
    context = {
        'form': form,
        'titulo': 'Importar Gerencias',
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/import_form.html', context)


# ===== ÁREAS =====

@login_required
def area_export(request):
    """Exportar áreas a Excel con plantilla y catálogos."""
    areas = filtrar_areas(request.user)
    
    excel_file = crear_plantilla_areas(areas)
    
    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=areas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return response


@login_required
def area_import(request):
    """Importar áreas desde Excel."""
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                df = pd.read_excel(archivo, sheet_name='Areas')
                
                columnas_requeridas = ['Nombre', 'Gerencia']
                if not all(col in df.columns for col in columnas_requeridas):
                    messages.error(request, 'El archivo debe contener: Nombre, Gerencia')
                    return redirect('area_import')
                
                creados = 0
                actualizados = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        nombre = str(row['Nombre']).strip()
                        gerencia_nombre = str(row['Gerencia']).strip()
                        
                        if not nombre or nombre == 'nan' or not gerencia_nombre or gerencia_nombre == 'nan':
                            continue
                        
                        # Buscar gerencia
                        try:
                            gerencia = Gerencia.objects.get(nombre=gerencia_nombre)
                        except Gerencia.DoesNotExist:
                            errores.append(f"Fila {idx + 2}: Gerencia '{gerencia_nombre}' no encontrada")
                            continue
                        
                        activa = True
                        if 'Activa' in row and pd.notna(row['Activa']):
                            activa = str(row['Activa']).strip().lower() in ['sí', 'si', 'yes', '1', 'true']
                        
                        area, created = Area.objects.update_or_create(
                            nombre=nombre,
                            gerencia=gerencia,
                            defaults={
                                'descripcion': row.get('Descripcion', '') if pd.notna(row.get('Descripcion')) else '',
                                'activa': activa,
                            }
                        )
                        
                        if created:
                            creados += 1
                        else:
                            actualizados += 1
                    
                    except Exception as e:
                        errores.append(f"Fila {idx + 2}: {str(e)}")
                
                if creados > 0:
                    messages.success(request, f'✓ {creados} áreas creadas')
                if actualizados > 0:
                    messages.info(request, f'ℹ {actualizados} áreas actualizadas')
                if errores:
                    for error in errores[:10]:
                        messages.warning(request, error)
                
                return redirect('area_list')
            
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
                return redirect('area_import')
    else:
        form = ImportExcelForm()
    
    # Si se solicita plantilla vacía, generarla y descargar
    if request.GET.get('plantilla') == 'vacia':
        excel_file = crear_plantilla_areas(None)
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=plantilla_areas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return response
    
    context = {
        'form': form,
        'titulo': 'Importar Áreas',
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/import_form.html', context)


# ===== PERSONAL =====

@login_required
def personal_export(request):
    """Exportar personal a Excel con plantilla y catálogos."""
    personal = filtrar_personal(request.user).select_related('area', 'area__gerencia')
    
    excel_file = crear_plantilla_personal(personal)
    
    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=personal_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    return response


@login_required
def personal_import(request):
    """Importar personal desde Excel."""
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                df = pd.read_excel(archivo, sheet_name='Personal')
                
                columnas_requeridas = ['NroDoc', 'ApellidosNombres']
                if not all(col in df.columns for col in columnas_requeridas):
                    messages.error(request, 'El archivo debe contener: NroDoc, ApellidosNombres')
                    return redirect('personal_import')
                
                creados = 0
                actualizados = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        nro_doc = str(row['NroDoc']).strip()
                        apellidos_nombres = str(row['ApellidosNombres']).strip()
                        
                        if not nro_doc or nro_doc == 'nan':
                            continue
                        
                        # Buscar área
                        area = None
                        if 'Area' in row and pd.notna(row['Area']):
                            try:
                                area = Area.objects.get(nombre=str(row['Area']).strip())
                            except Area.DoesNotExist:
                                pass
                        
                        # Preparar datos
                        datos = {
                            'apellidos_nombres': apellidos_nombres,
                            'tipo_doc': row.get('TipoDoc', 'DNI') if pd.notna(row.get('TipoDoc')) else 'DNI',
                            'codigo_fotocheck': row.get('CodigoFotocheck', '') if pd.notna(row.get('CodigoFotocheck')) else '',
                            'cargo': row.get('Cargo', '') if pd.notna(row.get('Cargo')) else '',
                            'tipo_trab': row.get('TipoTrabajador', 'Empleado') if pd.notna(row.get('TipoTrabajador')) else 'Empleado',
                            'area': area,
                            'estado': row.get('Estado', 'Activo') if pd.notna(row.get('Estado')) else 'Activo',
                            'sexo': row.get('Sexo', '') if pd.notna(row.get('Sexo')) else '',
                            'celular': row.get('Celular', '') if pd.notna(row.get('Celular')) else '',
                            'correo_personal': row.get('CorreoPersonal', '') if pd.notna(row.get('CorreoPersonal')) else '',
                            'correo_corporativo': row.get('CorreoCorporativo', '') if pd.notna(row.get('CorreoCorporativo')) else '',
                            'direccion': row.get('Direccion', '') if pd.notna(row.get('Direccion')) else '',
                            'ubigeo': row.get('Ubigeo', '') if pd.notna(row.get('Ubigeo')) else '',
                            'regimen_laboral': row.get('RegimenLaboral', '') if pd.notna(row.get('RegimenLaboral')) else '',
                            'regimen_turno': row.get('RegimenTurno', '') if pd.notna(row.get('RegimenTurno')) else '',
                            'observaciones': row.get('Observaciones', '') if pd.notna(row.get('Observaciones')) else '',
                        }
                        
                        # Fechas
                        if 'FechaAlta' in row and pd.notna(row['FechaAlta']):
                            try:
                                datos['fecha_alta'] = pd.to_datetime(row['FechaAlta']).date()
                            except (ValueError, TypeError):
                                pass
                        
                        if 'FechaCese' in row and pd.notna(row['FechaCese']):
                            try:
                                datos['fecha_cese'] = pd.to_datetime(row['FechaCese']).date()
                            except (ValueError, TypeError):
                                pass
                        
                        if 'FechaNacimiento' in row and pd.notna(row['FechaNacimiento']):
                            try:
                                datos['fecha_nacimiento'] = pd.to_datetime(row['FechaNacimiento']).date()
                            except (ValueError, TypeError):
                                pass
                        
                        # Decimales
                        if 'DiasLibresCorte2025' in row and pd.notna(row['DiasLibresCorte2025']):
                            try:
                                datos['dias_libres_corte_2025'] = Decimal(str(row['DiasLibresCorte2025']))
                            except (ValueError, TypeError, InvalidOperation):
                                pass
                        
                        # Crear o actualizar (DNI es la clave única)
                        personal_obj, created = Personal.objects.update_or_create(
                            nro_doc=nro_doc,
                            defaults=datos
                        )
                        
                        if created:
                            creados += 1
                        else:
                            actualizados += 1
                    
                    except Exception as e:
                        errores.append(f"Fila {idx + 2}: {str(e)}")
                
                if creados > 0:
                    messages.success(request, f'✓ {creados} personas creadas')
                if actualizados > 0:
                    messages.info(request, f'ℹ {actualizados} personas actualizadas')
                if errores:
                    for error in errores[:10]:
                        messages.warning(request, error)
                
                return redirect('personal_list')
            
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
                import traceback
                print(traceback.format_exc())
                return redirect('personal_import')
    else:
        form = ImportExcelForm()
    
    # Si se solicita plantilla vacía, generarla y descargar
    if request.GET.get('plantilla') == 'vacia':
        excel_file = crear_plantilla_personal(None)
        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=plantilla_personal_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return response
    
    context = {
        'form': form,
        'titulo': 'Importar Personal',
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/import_form.html', context)


# ===== ROSTER =====

@login_required
def roster_export(request):
    """Exportar roster a Excel con plantilla y catálogos."""
    mes = int(request.GET.get('mes', datetime.now().month))
    anio = int(request.GET.get('anio', datetime.now().year))
    
    primer_dia = datetime(anio, mes, 1).date()
    ultimo_dia = datetime(anio, mes, monthrange(anio, mes)[1]).date()
    
    personal_qs = filtrar_personal(request.user).filter(estado='Activo').order_by('apellidos_nombres')
    rosters = Roster.objects.filter(fecha__gte=primer_dia, fecha__lte=ultimo_dia, personal__in=personal_qs)
    
    excel_file = crear_plantilla_roster(mes, anio, personal_qs, rosters)
    
    response = HttpResponse(
        excel_file.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=roster_{anio}_{mes:02d}_{datetime.now().strftime("%H%M%S")}.xlsx'
    
    return response


@login_required
def roster_import(request):
    """Importar roster desde Excel."""
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                df = pd.read_excel(archivo, sheet_name='Roster')
                
                columnas_requeridas = ['DNI']
                if not all(col in df.columns for col in columnas_requeridas):
                    messages.error(request, 'El archivo debe contener la columna: DNI')
                    return redirect('roster_import')
                
                # Detectar mes y año (pedir al usuario o extraer del nombre del archivo)
                mes = int(request.POST.get('mes', datetime.now().month))
                anio = int(request.POST.get('anio', datetime.now().year))
                
                # Obtener columnas de días
                columnas_dias = [col for col in df.columns if col.startswith('Dia')]
                
                creados = 0
                actualizados = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        nro_doc = str(row['DNI']).strip()
                        if not nro_doc or nro_doc == 'nan':
                            continue
                        
                        personal = Personal.objects.get(nro_doc=nro_doc)
                        
                        # Procesar cada día
                        for col_dia in columnas_dias:
                            dia = int(col_dia.replace('Dia', '').strip())
                            codigo = str(row[col_dia]).strip().upper() if pd.notna(row[col_dia]) else ''
                            
                            if codigo and codigo != 'NAN':
                                fecha = datetime(anio, mes, dia).date()
                                
                                roster, created = Roster.objects.update_or_create(
                                    personal=personal,
                                    fecha=fecha,
                                    defaults={'codigo': codigo}
                                )
                                
                                if created:
                                    creados += 1
                                else:
                                    actualizados += 1
                    
                    except Personal.DoesNotExist:
                        errores.append(f"Fila {idx + 2}: Personal con DNI {nro_doc} no encontrado")
                    except Exception as e:
                        errores.append(f"Fila {idx + 2}: {str(e)}")
                
                if creados > 0:
                    messages.success(request, f'✓ {creados} registros creados')
                if actualizados > 0:
                    messages.info(request, f'ℹ {actualizados} registros actualizados')
                if errores:
                    for error in errores[:10]:
                        messages.warning(request, error)
                
                return redirect('roster_matricial')
            
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
                import traceback
                print(traceback.format_exc())
                return redirect('roster_import')
    else:
        form = ImportExcelForm()
    
    # Obtener mes y año actuales
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    
    context = {
        'form': form,
        'titulo': 'Importar Roster',
        'mes': mes_actual,
        'anio': anio_actual,
    }
    context.update(get_context_usuario(request.user))
    return render(request, 'personal/roster_import.html', context)


@login_required
@require_POST
def roster_update_cell(request):
    """Actualizar una celda del roster via AJAX."""
    try:
        data = json.loads(request.body)
        personal_id = data.get('personal_id')
        fecha_str = data.get('fecha')
        codigo = data.get('codigo', '').strip().upper()
        
        # Parsear fecha
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Buscar personal dentro del alcance del usuario
        personal = get_object_or_404(filtrar_personal(request.user), pk=personal_id)
        
        # Verificar permisos
        if not puede_editar_personal(request.user, personal):
            return JsonResponse({'success': False, 'error': 'No tienes permisos para editar este personal'}, status=403)
        
        # Validar que la fecha no sea anterior a la fecha de alta
        if personal.fecha_alta and fecha < personal.fecha_alta:
            return JsonResponse({
                'success': False, 
                'error': f'No se puede registrar antes de la fecha de alta ({personal.fecha_alta.strftime("%d/%m/%Y")})'
            }, status=400)
        
        if codigo:
            # Crear o actualizar roster
            roster, created = Roster.objects.update_or_create(
                personal=personal,
                fecha=fecha,
                defaults={'codigo': codigo}
            )
            mensaje = 'Registro creado' if created else 'Registro actualizado'
        else:
            # Eliminar si el código está vacío
            Roster.objects.filter(personal=personal, fecha=fecha).delete()
            mensaje = 'Registro eliminado'
        
        # Calcular días libres ganados y pendientes para retornar
        dias_libres_ganados = personal.dias_libres_ganados
        dias_dl_usados = personal.calcular_dias_dl_usados()
        dias_libres_pendientes = float(personal.dias_libres_corte_2025) + dias_libres_ganados - dias_dl_usados
        
        return JsonResponse({
            'success': True,
            'mensaje': mensaje,
            'codigo': codigo,
            'dias_libres_ganados': dias_libres_ganados,
            'dias_libres_pendientes': round(dias_libres_pendientes)
        })
    
    except Personal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Personal no encontrado'}, status=404)
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"ERROR EN roster_update_cell: {error_traceback}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
