"""
Configuración de logging estructurado para el sistema.
"""
import logging
import os
from pathlib import Path

# Directorio para logs
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Configuración de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {asctime} - {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_general': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'general.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'file_business': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'business.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
        'personal': {
            'handlers': ['console', 'file_general', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        'personal.security': {
            'handlers': ['console', 'file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
        'personal.business': {
            'handlers': ['console', 'file_business'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'file_general'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file_general', 'file_errors'],
        'level': 'INFO',
    },
}


def get_logger(name='personal'):
    """
    Obtiene un logger configurado.
    
    Args:
        name: Nombre del logger ('personal', 'personal.security', 'personal.business')
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)
