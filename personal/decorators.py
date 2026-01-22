"""
Decoradores para manejo robusto de excepciones en vistas.
"""
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse
from django.db import IntegrityError
import logging

logger = logging.getLogger('personal')
security_logger = logging.getLogger('personal.security')


def handle_exceptions(default_redirect='home'):
    """
    Decorador para manejo robusto de excepciones en vistas.
    
    Args:
        default_redirect: Vista a la que redirigir en caso de error
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            
            except PermissionDenied as e:
                security_logger.warning(
                    f"Acceso denegado: Usuario {request.user.username} "
                    f"intentó acceder a {view_func.__name__}. Error: {str(e)}"
                )
                messages.error(request, 'No tienes permisos para realizar esta acción.')
                return redirect(default_redirect)
            
            except ValidationError as e:
                logger.warning(f"Error de validación en {view_func.__name__}: {str(e)}")
                if hasattr(e, 'message_dict'):
                    for field, errors in e.message_dict.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")
                else:
                    messages.error(request, str(e))
                return redirect(default_redirect)
            
            except IntegrityError as e:
                logger.error(f"Error de integridad de BD en {view_func.__name__}: {str(e)}")
                messages.error(
                    request,
                    'Error de integridad de datos. Posible duplicado o violación de constraint.'
                )
                return redirect(default_redirect)
            
            except Exception as e:
                logger.exception(
                    f"Error inesperado en {view_func.__name__}: {str(e)}. "
                    f"Usuario: {request.user.username}"
                )
                messages.error(
                    request,
                    'Ha ocurrido un error inesperado. Por favor, contacta al administrador.'
                )
                return redirect(default_redirect)
        
        return wrapper
    return decorator


def handle_api_exceptions(view_func):
    """
    Decorador para manejo robusto de excepciones en API views.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        
        except PermissionDenied as e:
            security_logger.warning(
                f"API - Acceso denegado: Usuario {request.user.username} "
                f"intentó acceder a {view_func.__name__}. Error: {str(e)}"
            )
            return JsonResponse(
                {'error': 'No tienes permisos para realizar esta acción.'},
                status=403
            )
        
        except ValidationError as e:
            logger.warning(f"API - Error de validación en {view_func.__name__}: {str(e)}")
            if hasattr(e, 'message_dict'):
                return JsonResponse(
                    {'error': 'Error de validación', 'details': e.message_dict},
                    status=400
                )
            return JsonResponse({'error': str(e)}, status=400)
        
        except IntegrityError as e:
            logger.error(f"API - Error de integridad en {view_func.__name__}: {str(e)}")
            return JsonResponse(
                {'error': 'Error de integridad de datos. Posible duplicado.'},
                status=400
            )
        
        except Exception as e:
            logger.exception(
                f"API - Error inesperado en {view_func.__name__}: {str(e)}. "
                f"Usuario: {request.user.username}"
            )
            return JsonResponse(
                {'error': 'Error interno del servidor'},
                status=500
            )
    
    return wrapper


def log_access(action_description):
    """
    Decorador para registrar accesos a vistas sensibles.
    
    Args:
        action_description: Descripción de la acción
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            security_logger.info(
                f"{action_description} - Usuario: {request.user.username}, "
                f"IP: {request.META.get('REMOTE_ADDR')}, "
                f"Vista: {view_func.__name__}"
            )
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
