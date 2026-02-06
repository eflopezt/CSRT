"""
Validadores centralizados de lógica de negocio.
"""
from decimal import Decimal, InvalidOperation
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
import logging

logger = logging.getLogger('personal.business')


class PersonalValidator:
    """Validador para el modelo Personal."""
    
    @staticmethod
    def validar_nro_doc(nro_doc, tipo_doc='DNI'):
        """
        Valida el número de documento según el tipo.
        
        Args:
            nro_doc: Número de documento a validar
            tipo_doc: Tipo de documento ('DNI', 'CE', 'Pasaporte')
        
        Raises:
            ValidationError: Si el documento no es válido
        """
        if not nro_doc:
            raise ValidationError(_('El número de documento es obligatorio.'))
        
        nro_doc = str(nro_doc).strip()
        
        if tipo_doc == 'DNI':
            if not re.match(r'^\d{8}$', nro_doc):
                raise ValidationError(_('El DNI debe tener exactamente 8 dígitos.'))
        elif tipo_doc == 'CE':
            if not re.match(r'^\d{9,12}$', nro_doc):
                raise ValidationError(_('El CE debe tener entre 9 y 12 dígitos.'))
        elif tipo_doc == 'Pasaporte':
            if len(nro_doc) < 5 or len(nro_doc) > 20:
                raise ValidationError(_('El Pasaporte debe tener entre 5 y 20 caracteres.'))
        
        logger.info(f"Documento validado: {tipo_doc} - {nro_doc}")
        return nro_doc
    
    @staticmethod
    def validar_regimen_turno(regimen_turno):
        """
        Valida el formato del régimen de turno (NxM).
        
        Args:
            regimen_turno: Régimen en formato "21x7", "15x3", etc.
        
        Returns:
            tuple: (dias_trabajo, dias_descanso) si es válido
        
        Raises:
            ValidationError: Si el formato no es válido
        """
        if not regimen_turno:
            return None
        
        regimen_turno = regimen_turno.strip()
        
        # Validar formato NxM
        if not re.match(r'^\d{1,2}x\d{1,2}$', regimen_turno):
            raise ValidationError(
                _('El régimen de turno debe estar en formato NxM (ejemplo: 21x7, 14x7)')
            )
        
        try:
            partes = regimen_turno.split('x')
            dias_trabajo = int(partes[0])
            dias_descanso = int(partes[1])
            
            # Validaciones de negocio
            if dias_trabajo < 1 or dias_trabajo > 31:
                raise ValidationError(_('Los días de trabajo deben estar entre 1 y 31.'))
            
            if dias_descanso < 1 or dias_descanso > 31:
                raise ValidationError(_('Los días de descanso deben estar entre 1 y 31.'))
            
            if dias_trabajo < dias_descanso:
                logger.warning(
                    f"Régimen inusual detectado: {regimen_turno} "
                    f"(días trabajo < días descanso)"
                )
            
            logger.info(f"Régimen de turno validado: {regimen_turno}")
            return (dias_trabajo, dias_descanso)
            
        except (ValueError, IndexError) as e:
            raise ValidationError(_(f'Error al procesar el régimen de turno: {str(e)}'))
    
    @staticmethod
    def validar_rango_fechas(fecha_inicio, fecha_fin=None):
        """
        Valida un rango de fechas.
        
        Args:
            fecha_inicio: Fecha de inicio
            fecha_fin: Fecha de fin (opcional)
        
        Raises:
            ValidationError: Si las fechas no son válidas
        """
        if not fecha_inicio:
            raise ValidationError(_('La fecha de inicio es obligatoria.'))
        
        if isinstance(fecha_inicio, str):
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError(_('Formato de fecha de inicio inválido. Use YYYY-MM-DD.'))
        
        if fecha_fin:
            if isinstance(fecha_fin, str):
                try:
                    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                except ValueError:
                    raise ValidationError(_('Formato de fecha de fin inválido. Use YYYY-MM-DD.'))
            
            if fecha_fin < fecha_inicio:
                raise ValidationError(
                    _('La fecha de fin no puede ser anterior a la fecha de inicio.')
                )
        
        return fecha_inicio, fecha_fin
    
    @staticmethod
    def validar_monto(monto, campo='monto', minimo=0, maximo=None):
        """
        Valida un monto monetario.
        
        Args:
            monto: Monto a validar
            campo: Nombre del campo (para mensajes)
            minimo: Valor mínimo permitido
            maximo: Valor máximo permitido (opcional)
        
        Returns:
            Decimal: Monto validado
        
        Raises:
            ValidationError: Si el monto no es válido
        """
        if monto is None:
            return None
        
        try:
            monto = Decimal(str(monto))
        except (ValueError, InvalidOperation):
            raise ValidationError(_(f'El {campo} debe ser un número válido.'))
        
        if monto < minimo:
            raise ValidationError(_(f'El {campo} no puede ser menor a {minimo}.'))
        
        if maximo and monto > maximo:
            raise ValidationError(_(f'El {campo} no puede ser mayor a {maximo}.'))
        
        return monto


class RosterValidator:
    """Validador para el modelo Roster."""
    
    CODIGOS_VALIDOS = ['T', 'TR', 'D', 'V', 'L', 'S', 'F', 'P', 'DM', 'DS', 'DL', 'DLA', 'DOL', 'FC']
    
    @staticmethod
    def validar_codigo(codigo):
        """
        Valida que el código de roster sea válido.
        
        Args:
            codigo: Código a validar
        
        Raises:
            ValidationError: Si el código no es válido
        """
        if not codigo:
            raise ValidationError(_('El código de roster es obligatorio.'))
        
        codigo = codigo.strip().upper()
        
        if codigo not in RosterValidator.CODIGOS_VALIDOS:
            raise ValidationError(
                _(f'Código inválido. Códigos válidos: {", ".join(RosterValidator.CODIGOS_VALIDOS)}')
            )
        
        return codigo
    
    @staticmethod
    def validar_fecha_edicion(fecha, usuario):
        """
        Valida si la fecha puede ser editada según permisos del usuario.
        
        Args:
            fecha: Fecha del roster
            usuario: Usuario que intenta editar
        
        Raises:
            ValidationError: Si la fecha no puede ser editada
        """
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError(_('Formato de fecha inválido.'))
        
        # Los administradores pueden editar cualquier fecha
        if usuario.is_superuser:
            return True
        
        # Los demás solo pueden editar del día actual en adelante
        hoy = date.today()
        if fecha < hoy:
            raise ValidationError(
                _('No puedes editar fechas pasadas. Solo puedes editar desde hoy en adelante.')
            )
        
        logger.info(f"Usuario {usuario.username} editando fecha {fecha}")
        return True
    
    @staticmethod
    def validar_duplicado(personal, fecha, roster_id=None):
        """
        Valida que no exista un registro duplicado.
        
        Args:
            personal: Instancia de Personal
            fecha: Fecha del roster
            roster_id: ID del roster actual (para actualizaciones)
        
        Raises:
            ValidationError: Si existe un duplicado
        """
        from .models import Roster
        
        query = Roster.objects.filter(personal=personal, fecha=fecha)
        
        if roster_id:
            query = query.exclude(pk=roster_id)
        
        if query.exists():
            raise ValidationError(
                _(f'Ya existe un registro de roster para {personal.apellidos_nombres} '
                  f'en la fecha {fecha}.')
            )
        
        return True


class AreaValidator:
    """Validador para el modelo Area."""
    
    @staticmethod
    def validar_responsable_unico(responsable, area_id=None):
        """
        Valida que el responsable sea válido.
        
        Args:
            responsable: Instancia de Personal
            area_id: ID del area actual (para actualizaciones)
        
        Returns:
            bool: Siempre True (compatibilidad)
        """
        if not responsable:
            return True

        logger.info(f"Responsable validado: {responsable.apellidos_nombres}")
        return True


def validar_archivo_excel(archivo):
    """
    Valida que un archivo sea un Excel válido.
    
    Args:
        archivo: Archivo subido (UploadedFile)
    
    Raises:
        ValidationError: Si el archivo no es válido
    """
    # Validar extensión
    nombre = archivo.name.lower()
    extensiones_validas = ['.xlsx', '.xls']
    
    if not any(nombre.endswith(ext) for ext in extensiones_validas):
        raise ValidationError(
            _(f'El archivo debe ser Excel ({", ".join(extensiones_validas)}).')
        )
    
    # Validar tamaño (máximo 10MB)
    max_size = 10 * 1024 * 1024  # 10MB en bytes
    if archivo.size > max_size:
        raise ValidationError(
            _(f'El archivo es muy grande. Tamaño máximo: {max_size / (1024*1024):.0f}MB.')
        )
    
    # Validar que el archivo no esté vacío
    if archivo.size == 0:
        raise ValidationError(_('El archivo está vacío.'))
    
    logger.info(f"Archivo Excel validado: {archivo.name} ({archivo.size} bytes)")
    return True
