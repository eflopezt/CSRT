"""
Tareas asíncronas con Celery para el módulo personal.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import pandas as pd
from datetime import datetime
from .models import Personal, Roster


@shared_task
def procesar_import_excel(archivo_path, tipo_import):
    """
    Procesar importación de archivos Excel de forma asíncrona.
    
    Args:
        archivo_path: Ruta del archivo a procesar
        tipo_import: 'personal' o 'roster'
    
    Returns:
        dict con resultados de la importación
    """
    try:
        df = pd.read_excel(archivo_path)
        creados = 0
        actualizados = 0
        errores = []
        
        if tipo_import == 'personal':
            for idx, row in df.iterrows():
                try:
                    nro_doc = str(row.get('NroDoc', '')).strip()
                    if not nro_doc:
                        continue
                    
                    personal, created = Personal.objects.update_or_create(
                        nro_doc=nro_doc,
                        defaults={
                            'apellidos_nombres': row.get('ApellidosNombres', ''),
                            'cargo': row.get('Cargo', ''),
                            'tipo_trab': row.get('TipoTrabajador', 'Empleado'),
                            'celular': row.get('Celular', ''),
                            'correo_personal': row.get('Correo', ''),
                        }
                    )
                    
                    if created:
                        creados += 1
                    else:
                        actualizados += 1
                        
                except Exception as e:
                    errores.append(f"Fila {idx + 2}: {str(e)}")
        
        elif tipo_import == 'roster':
            for idx, row in df.iterrows():
                try:
                    nro_doc = str(row.get('NroDoc', '')).strip()
                    fecha = pd.to_datetime(row.get('Fecha')).date()
                    
                    personal = Personal.objects.get(nro_doc=nro_doc)
                    
                    roster, created = Roster.objects.update_or_create(
                        personal=personal,
                        fecha=fecha,
                        defaults={
                            'codigo': row.get('Codigo', ''),
                            'dias_libres_ganados': row.get('DiasLibresGanados', 0),
                            'fuente': f'Import Excel {datetime.now().strftime("%Y-%m-%d")}',
                        }
                    )
                    
                    if created:
                        creados += 1
                    else:
                        actualizados += 1
                        
                except Personal.DoesNotExist:
                    errores.append(f"Fila {idx + 2}: Personal con DNI {nro_doc} no encontrado")
                except Exception as e:
                    errores.append(f"Fila {idx + 2}: {str(e)}")
        
        return {
            'success': True,
            'creados': creados,
            'actualizados': actualizados,
            'errores': errores
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@shared_task
def generar_reporte_mensual(mes, anio):
    """
    Generar reporte mensual de asistencias.
    
    Args:
        mes: Número del mes (1-12)
        anio: Año
    
    Returns:
        dict con ruta del archivo generado
    """
    from datetime import date
    
    try:
        fecha_inicio = date(anio, mes, 1)
        if mes == 12:
            fecha_fin = date(anio + 1, 1, 1)
        else:
            fecha_fin = date(anio, mes + 1, 1)
        
        roster = Roster.objects.filter(
            fecha__gte=fecha_inicio,
            fecha__lt=fecha_fin
        ).select_related('personal', 'personal__area')
        
        data = []
        for r in roster:
            data.append({
                'Fecha': r.fecha,
                'DNI': r.personal.nro_doc,
                'Nombres': r.personal.apellidos_nombres,
                'Area': r.personal.area.nombre if r.personal.area else '',
                'Codigo': r.codigo,
                'DiasLibresGanados': float(r.dias_libres_ganados),
            })
        
        df = pd.DataFrame(data)
        filename = f'reporte_{anio}_{mes:02d}.xlsx'
        filepath = f'/tmp/{filename}'
        
        df.to_excel(filepath, index=False)
        
        return {
            'success': True,
            'filepath': filepath,
            'filename': filename
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@shared_task
def enviar_notificacion_email(asunto, mensaje, destinatarios):
    """
    Enviar notificación por email.
    
    Args:
        asunto: Asunto del email
        mensaje: Contenido del mensaje
        destinatarios: Lista de emails
    """
    try:
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            destinatarios,
            fail_silently=False,
        )
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}


@shared_task
def limpiar_datos_antiguos(dias=365):
    """
    Limpiar registros de auditoría antiguos.
    
    Args:
        dias: Días de antigüedad para eliminar
    """
    from datetime import timedelta
    from .models import RosterAudit
    
    fecha_limite = datetime.now() - timedelta(days=dias)
    eliminados = RosterAudit.objects.filter(creado_en__lt=fecha_limite).delete()
    
    return {
        'success': True,
        'eliminados': eliminados[0]
    }
