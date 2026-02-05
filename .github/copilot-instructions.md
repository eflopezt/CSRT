# Instrucciones del Proyecto - Gestión Personal

## ✅ Progreso de Configuración

- [x] Crear estructura de directorios base
- [x] Configurar proyecto Django con settings modulares
- [x] Crear modelos de datos
- [x] Configurar Django REST Framework
- [x] Crear requirements y Docker
- [x] Configurar herramientas de desarrollo
- [x] Crear vistas y templates
- [x] Configurar Celery y Redis
- [x] Instalar dependencias
- [x] Crear comandos de management

## Descripción del Proyecto

Sistema de gestión de personal simplificado con las siguientes características:

### Modelos de Datos:
1. **Area**: Áreas o departamentos de alto nivel (1 responsable)
2. **SubArea**: SubÁreas bajo áreas
3. **Personal**: Personal disponible con datos completos
4. **Roster**: Programación de turnos con días libres ganados

### Stack Tecnológico:
- Django 6.0 + Python 3.12
- Django REST Framework
- Redis + Celery
- PostgreSQL
- pytest + ruff + black
- Docker
