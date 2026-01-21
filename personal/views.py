"""
Vistas para el módulo personal.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from datetime import datetime, timedelta
from calendar import monthrange
from collections import defaultdict
import json

from .models import Gerencia, Area, Personal, Roster, RosterAudit
from .forms import GerenciaForm, AreaForm, PersonalForm, RosterForm, ImportExcelForm


@login_required
def home(request):
    """Vista principal del sistema."""
    context = {
        'total_gerencias': Gerencia.objects.filter(activa=True).count(),
        'total_areas': Area.objects.filter(activa=True).count(),
        'total_personal': Personal.objects.filter(estado='Activo').count(),
        'total_roster_hoy': Roster.objects.filter(fecha=datetime.now().date()).count(),
    }
    return render(request, 'home.html', context)


# ================== GERENCIAS ==================

@login_required
def gerencia_list(request):
    """Lista de gerencias."""
    gerencias = Gerencia.objects.all().annotate(
        total_areas=Count('areas'),
    ).order_by('nombre')
    
    # Filtros
    buscar = request.GET.get('buscar', '')
    if buscar:
        gerencias = gerencias.filter(
            Q(nombre__icontains=buscar) |
            Q(responsable__apellidos_nombres__icontains=buscar)
        )
    
    return render(request, 'personal/gerencia_list.html', {
        'gerencias': gerencias,
        'buscar': buscar
    })


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
    areas = Area.objects.select_related('gerencia').annotate(
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
    personal = Personal.objects.select_related('area', 'area__gerencia').order_by('apellidos_nombres')
    
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
    personal = get_object_or_404(Personal, pk=pk)
    
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=personal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal actualizado exitosamente.')
            return redirect('personal_list')
    else:
        form = PersonalForm(instance=personal)
    
    return render(request, 'personal/personal_form.html', {
        'form': form,
        'personal': personal
    })


@login_required
def personal_detail(request, pk):
    """Detalle de personal."""
    personal = get_object_or_404(
        Personal.objects.select_related('area', 'area__gerencia'),
        pk=pk
    )
    
    # Últimos registros de roster
    roster_reciente = Roster.objects.filter(personal=personal).order_by('-fecha')[:10]
    
    return render(request, 'personal/personal_detail.html', {
        'personal': personal,
        'roster_reciente': roster_reciente
    })


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
    
    # Obtener personal activo
    personal_qs = Personal.objects.filter(estado='Activo').select_related('area', 'area__gerencia')
    
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
        
        # Calcular días trabajados: contar códigos T y TR
        count_t = sum(1 for item in codigos_mes if item['codigo'] == 'T')
        count_tr = sum(1 for item in codigos_mes if item['codigo'] == 'TR')
        
        # T: cada 3 genera 1 día libre, TR: cada 5 genera 2 días libres
        dias_libres_t = count_t // 3
        dias_libres_tr = (count_tr // 5) * 2
        dias_trabajados_calculados = dias_libres_t + dias_libres_tr
        
        fila = {
            'personal': persona,
            'dias_libres_corte_2025': persona.dias_libres_corte_2025,
            'dias_libres_pendientes': dias_trabajados_calculados,
            'dias_trabajados': dias_trabajados_calculados,
            'count_t': count_t,
            'count_tr': count_tr,
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

@login_required
def personal_export(request):
    """Exportar personal a Excel."""
    personal = Personal.objects.select_related('area', 'area__gerencia').all()
    
    data = []
    for p in personal:
        data.append({
            'NroDoc': p.nro_doc,
            'ApellidosNombres': p.apellidos_nombres,
            'Cargo': p.cargo,
            'TipoTrabajador': p.tipo_trab,
            'Area': p.area.nombre if p.area else '',
            'Gerencia': p.area.gerencia.nombre if p.area and p.area.gerencia else '',
            'Estado': p.estado,
            'FechaAlta': p.fecha_alta,
            'Celular': p.celular,
            'CorreoCorporativo': p.correo_corporativo,
            'Banco': p.banco,
            'CuentaAhorros': p.cuenta_ahorros,
        })
    
    df = pd.DataFrame(data)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=personal_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Personal')
    
    return response


@login_required
def roster_export(request):
    """Exportar roster a Excel."""
    mes = int(request.GET.get('mes', datetime.now().month))
    anio = int(request.GET.get('anio', datetime.now().year))
    
    primer_dia = datetime(anio, mes, 1).date()
    ultimo_dia = datetime(anio, mes, monthrange(anio, mes)[1]).date()
    
    # Obtener datos
    personal_qs = Personal.objects.filter(estado='Activo').select_related('area', 'area__gerencia').order_by('apellidos_nombres')
    rosters = Roster.objects.filter(fecha__gte=primer_dia, fecha__lte=ultimo_dia, personal__in=personal_qs).select_related('personal')
    
    # Organizar por personal y fecha
    roster_dict = defaultdict(dict)
    for r in rosters:
        roster_dict[r.personal_id][r.fecha.day] = r.codigo
    
    # Generar días del mes
    dias = list(range(1, monthrange(anio, mes)[1] + 1))
    
    # Construir datos
    data = []
    for persona in personal_qs:
        fila = {
            'DNI': persona.nro_doc,
            'Apellidos y Nombres': persona.apellidos_nombres,
            'Área': persona.area.nombre if persona.area else '',
            'Días Libres al 31/12/25': persona.dias_libres_corte_2025,
        }
        # Agregar códigos por día
        for dia in dias:
            fecha = datetime(anio, mes, dia).date()
            codigo = roster_dict[persona.id].get(dia, '')
            fila[f'Día {dia:02d}'] = codigo
        
        # Calcular días trabajados
        codigos_numericos = sum(1 for d in dias if str(roster_dict[persona.id].get(d, '')).isdigit())
        fila['Días Trabajados'] = round(codigos_numericos / 3) if codigos_numericos > 0 else 0
        
        data.append(fila)
    
    df = pd.DataFrame(data)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=roster_{anio}_{mes:02d}.xlsx'
    
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Roster')
    
    return response


@login_required
def roster_import(request):
    """Importar roster desde Excel."""
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                # Leer Excel
                df = pd.read_excel(archivo)
                
                # Validar columnas requeridas
                columnas_requeridas = ['DNI', 'Apellidos y Nombres']
                if not all(col in df.columns for col in columnas_requeridas):
                    messages.error(request, 'El archivo debe contener las columnas: DNI, Apellidos y Nombres, y Día 01, Día 02, etc.')
                    return redirect('roster_import')
                
                # Obtener columnas de días
                columnas_dias = [col for col in df.columns if col.startswith('Día ')]
                
                registros_creados = 0
                registros_actualizados = 0
                errores = []
                
                for idx, row in df.iterrows():
                    try:
                        # Buscar personal por DNI
                        personal = Personal.objects.get(nro_doc=str(row['DNI']).strip())
                        
                        # Procesar cada día
                        for col_dia in columnas_dias:
                            # Extraer número de día
                            dia = int(col_dia.replace('Día ', '').strip())
                            codigo = str(row[col_dia]).strip() if pd.notna(row[col_dia]) else ''
                            
                            if codigo and codigo != 'nan':
                                # Determinar fecha (usar mes/año del formulario o actual)
                                mes = datetime.now().month
                                anio = datetime.now().year
                                fecha = datetime(anio, mes, dia).date()
                                
                                # Crear o actualizar roster
                                roster, created = Roster.objects.update_or_create(
                                    personal=personal,
                                    fecha=fecha,
                                    defaults={'codigo': codigo}
                                )
                                
                                if created:
                                    registros_creados += 1
                                else:
                                    registros_actualizados += 1
                    
                    except Personal.DoesNotExist:
                        errores.append(f"Fila {idx + 2}: Personal con DNI {row['DNI']} no encontrado")
                    except Exception as e:
                        errores.append(f"Fila {idx + 2}: {str(e)}")
                
                # Mensajes de resultado
                if registros_creados > 0:
                    messages.success(request, f'{registros_creados} registros creados.')
                if registros_actualizados > 0:
                    messages.info(request, f'{registros_actualizados} registros actualizados.')
                if errores:
                    for error in errores[:10]:  # Mostrar máximo 10 errores
                        messages.warning(request, error)
                
                return redirect('roster_matricial')
            
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')
                return redirect('roster_import')
    else:
        form = ImportExcelForm()
    
    return render(request, 'personal/roster_import.html', {'form': form})


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
        
        # Buscar personal
        personal = Personal.objects.get(pk=personal_id)
        
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
        
        # Calcular días libres pendientes para retornar
        rosters_personal = Roster.objects.filter(personal=personal)
        count_t = rosters_personal.filter(codigo='T').count()
        count_tr = rosters_personal.filter(codigo='TR').count()
        
        dias_libres_t = count_t // 3
        dias_libres_tr = (count_tr // 5) * 2
        dias_libres_pendientes = dias_libres_t + dias_libres_tr
        
        return JsonResponse({
            'success': True,
            'mensaje': mensaje,
            'codigo': codigo,
            'dias_libres_pendientes': dias_libres_pendientes
        })
    
    except Personal.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Personal no encontrado'}, status=404)
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"ERROR EN roster_update_cell: {error_traceback}")
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
