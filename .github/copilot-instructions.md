# Instrucciones del Proyecto - Gestión Personal

## ✅ Progreso de Configuración

- [x] Crear estructura de directorios base
- [ ] Configurar proyecto Django con settings modulares
- [ ] Crear modelos de datos
- [ ] Configurar Django REST Framework
- [ ] Crear requirements y Docker
- [ ] Configurar herramientas de desarrollo
- [ ] Crear vistas y templates
- [ ] Configurar Celery y Redis
- [ ] Instalar dependencias
- [ ] Crear comandos de management

## Descripción del Proyecto

Sistema de gestión de personal simplificado con las siguientes características:

### Modelos de Datos:
1. **Gerencia**: Departamentos de alto nivel (1 responsable)
2. **Area**: Áreas bajo gerencias
3. **Personal**: Personal disponible con datos completos
4. **Roster**: Programación de turnos con días libres ganados

### Stack Tecnológico:
- Django 6.0 + Python 3.12
- Django REST Framework
- Redis + Celery
- PostgreSQL
- pytest + ruff + black
- Docker
