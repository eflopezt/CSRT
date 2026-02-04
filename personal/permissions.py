"""
Utilidades para manejo de permisos y filtros por usuario.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Area, SubArea, Personal


def es_responsable_area(user):
    """Verifica si el usuario es responsable de un área."""
    if user.is_superuser:
        return False
    return user.groups.filter(name='Responsable de Área').exists()


def get_area_responsable(user):
    """Obtiene el área de la que el usuario es responsable."""
    try:
        personal = user.personal_data
        area = Area.objects.get(responsable=personal)
        return area
    except (AttributeError, Area.DoesNotExist, Personal.DoesNotExist):
        return None


def filtrar_areas(user):
    """Filtra áreas según el usuario."""
    # Todos los usuarios pueden ver todas las áreas (son catálogos)
    # La restricción de edición se hace a nivel de vista
    return Area.objects.all()


def filtrar_subareas(user):
    """Filtra subáreas según el usuario."""
    if user.is_superuser:
        return SubArea.objects.all()
    
    area = get_area_responsable(user)
    if area:
        return SubArea.objects.filter(area=area)
    
    return SubArea.objects.none()


def filtrar_personal(user):
    """Filtra personal según el usuario."""
    if user.is_superuser:
        return Personal.objects.all()
    
    # Si el usuario tiene un Personal vinculado, puede ver su propio registro
    if hasattr(user, 'personal_data') and user.personal_data:
        # Si también es responsable, ve su área completa
        area = get_area_responsable(user)
        if area:
            return Personal.objects.filter(subarea__area=area)
        # Si solo es personal regular, solo ve su propio registro
        return Personal.objects.filter(id=user.personal_data.id)
    
    # Si es responsable sin Personal vinculado (caso legacy)
    area = get_area_responsable(user)
    if area:
        return Personal.objects.filter(subarea__area=area)
    
    return Personal.objects.none()


def puede_editar_personal(user, personal):
    """Verifica si el usuario puede editar un personal específico."""
    if user.is_superuser:
        return True
    
    # Un usuario puede editar su propio registro de Personal
    if hasattr(user, 'personal_data') and user.personal_data and user.personal_data == personal:
        return True
    
    # Un responsable puede editar el personal de su área
    area = get_area_responsable(user)
    if area and personal.subarea and personal.subarea.area == area:
        return True
    
    return False


def solo_responsable(view_func):
    """
    Decorador que restringe el acceso solo a responsables de area.
    Los superusuarios también tienen acceso.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or es_responsable_area(request.user):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    return wrapper


def get_context_usuario(user):
    """
    Retorna contexto común para el usuario (gerencia, es_responsable, etc).
    """
    es_responsable = es_responsable_area(user)
    area = get_area_responsable(user) if es_responsable else None
    
    return {
        'es_responsable': es_responsable,
        'area_responsable': area,
        'es_superusuario': user.is_superuser,
    }
