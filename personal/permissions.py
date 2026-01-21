"""
Utilidades para manejo de permisos y filtros por usuario.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Gerencia, Area, Personal


def es_responsable_gerencia(user):
    """Verifica si el usuario es responsable de una gerencia."""
    if user.is_superuser:
        return False
    return user.groups.filter(name='Responsable de Gerencia').exists()


def get_gerencia_responsable(user):
    """Obtiene la gerencia de la que el usuario es responsable."""
    try:
        personal = user.personal_data
        gerencia = Gerencia.objects.get(responsable=personal)
        return gerencia
    except (AttributeError, Gerencia.DoesNotExist, Personal.DoesNotExist):
        return None


def filtrar_gerencias(user):
    """Filtra gerencias según el usuario."""
    if user.is_superuser:
        return Gerencia.objects.all()
    
    gerencia = get_gerencia_responsable(user)
    if gerencia:
        return Gerencia.objects.filter(id=gerencia.id)
    
    return Gerencia.objects.none()


def filtrar_areas(user):
    """Filtra áreas según el usuario."""
    if user.is_superuser:
        return Area.objects.all()
    
    gerencia = get_gerencia_responsable(user)
    if gerencia:
        return Area.objects.filter(gerencia=gerencia)
    
    return Area.objects.none()


def filtrar_personal(user):
    """Filtra personal según el usuario."""
    if user.is_superuser:
        return Personal.objects.all()
    
    gerencia = get_gerencia_responsable(user)
    if gerencia:
        return Personal.objects.filter(area__gerencia=gerencia)
    
    return Personal.objects.none()


def puede_editar_personal(user, personal):
    """Verifica si el usuario puede editar un personal específico."""
    if user.is_superuser:
        return True
    
    gerencia = get_gerencia_responsable(user)
    if gerencia and personal.area and personal.area.gerencia == gerencia:
        return True
    
    return False


def solo_responsable(view_func):
    """
    Decorador que restringe el acceso solo a responsables de gerencia.
    Los superusuarios también tienen acceso.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or es_responsable_gerencia(request.user):
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    return wrapper


def get_context_usuario(user):
    """
    Retorna contexto común para el usuario (gerencia, es_responsable, etc).
    """
    es_responsable = es_responsable_gerencia(user)
    gerencia = get_gerencia_responsable(user) if es_responsable else None
    
    return {
        'es_responsable': es_responsable,
        'gerencia_responsable': gerencia,
        'es_superusuario': user.is_superuser,
    }
