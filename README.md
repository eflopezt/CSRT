# 🚀 Sistema de Gestión de Personal

Sistema moderno de gestión de recursos humanos desarrollado con Django 6.0 y tecnologías de vanguardia.

## 📋 Características

- ✅ **Gestión de Gerencias y Áreas**: Estructura organizacional jerárquica
- ✅ **Gestión de Personal**: Control completo de datos del personal disponible
- ✅ **Roster Inteligente**: Programación de turnos con días libres ganados
- ✅ **API REST**: Endpoints completos con Django REST Framework
- ✅ **Caché con Redis**: Rendimiento optimizado
- ✅ **Tareas Asíncronas**: Procesamiento con Celery
- ✅ **Tests Automatizados**: Suite de pruebas con pytest
- ✅ **Código Limpio**: Ruff + Black + isort
- ✅ **Docker Ready**: Despliegue con docker-compose

## 🛠️ Stack Tecnológico

### Backend
- **Django 6.0**: Framework web moderno
- **Python 3.12**: Última versión estable
- **PostgreSQL**: Base de datos relacional (producción)
- **SQLite**: Base de datos para desarrollo

### API & Frontend
- **Django REST Framework**: API RESTful
- **Bootstrap 5**: Framework CSS moderno
- **DataTables**: Tablas interactivas
- **jQuery**: Interactividad

### Performance & Cache
- **Redis**: Sistema de caché
- **Django-Redis**: Integración con Django
- **WhiteNoise**: Servir archivos estáticos

### Async Tasks
- **Celery**: Cola de tareas asíncronas
- **Redis**: Message broker

### Development Tools
- **pytest**: Framework de testing
- **ruff**: Linter super rápido
- **black**: Formateador de código
- **isort**: Ordenar imports
- **django-debug-toolbar**: Debugging

### Monitoring
- **Sentry**: Monitoreo de errores (producción)

## 🚀 Inicio Rápido

### Opción 1: Sin Docker (Local)

```bash
# 1. Clonar y acceder al directorio
cd gestion-personal-nuevo

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar variables de entorno
cp .env.example .env

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario y datos de prueba
python manage.py seed_data --with-roster

# 7. Ejecutar servidor
python manage.py runserver
```

Acceder a: **http://localhost:8000**

**Credenciales:**
- Usuario: `admin`
- Contraseña: `admin123`

### Opción 2: Con Docker

```bash
# 1. Construir y levantar servicios
docker-compose up -d

# 2. Ejecutar migraciones
docker-compose exec web python manage.py migrate

# 3. Crear datos de prueba
docker-compose exec web python manage.py seed_data --with-roster

# 4. Ver logs
docker-compose logs -f web
```

Acceder a: **http://localhost:8000**

## 📁 Estructura del Proyecto

```
gestion-personal-nuevo/
├── config/                 # Configuración del proyecto
│   ├── settings/
│   │   ├── base.py        # Settings comunes
│   │   ├── development.py # Settings desarrollo
│   │   └── production.py  # Settings producción
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py          # Configuración Celery
│
├── personal/              # App principal
│   ├── models.py          # Modelos (Gerencia, Area, Personal, Roster)
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # Vistas web
│   ├── api_views.py       # Vistas API
│   ├── urls.py            # URLs web
│   ├── api_urls.py        # URLs API
│   ├── forms.py           # Formularios
│   ├── admin.py           # Django admin
│   ├── tasks.py           # Tareas Celery
│   ├── signals.py         # Signals
│   ├── management/        # Comandos personalizados
│   └── tests/             # Tests
│
├── templates/             # Templates HTML
│   ├── base.html
│   ├── home.html
│   └── registration/
│
├── static/                # Archivos estáticos
├── staticfiles/           # Archivos estáticos recopilados
├── media/                 # Archivos subidos
│
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Docker container
├── docker-compose.yml    # Orquestación Docker
├── pyproject.toml        # Configuración ruff/black/pytest
├── pytest.ini            # Configuración pytest
├── .env.example          # Variables de entorno ejemplo
├── .gitignore
└── README.md
```

## 🗄️ Modelos de Datos

### Gerencia
- **Campos**: nombre, responsable (OneToOne), descripción, activa
- **Relaciones**: N áreas

### Area
- **Campos**: nombre, gerencia (FK), descripción, activa
- **Relaciones**: N personal

### Personal
- **Campos**: 
  - Identificación: tipo_doc, nro_doc, apellidos_nombres, codigo_fotocheck
  - Laborales: cargo, tipo_trab, area (FK), fecha_alta, fecha_cese, estado
  - Personales: fecha_nacimiento, sexo, celular, correos, dirección
  - Financieros: afp, banco, cuentas bancarias, sueldo, bonos
  - Régimen: regimen_laboral, regimen_turno
- **Relaciones**: N roster_dias

### Roster
- **Campos**: personal (FK), fecha, codigo, **dias_libres_ganados**, observaciones
- **Constraint**: Unique (personal, fecha)

### RosterAudit
- **Campos**: personal, fecha, campo_modificado, valor_anterior, valor_nuevo, usuario
- **Propósito**: Auditoría automática de cambios

## 🔌 API Endpoints

### Gerencias
- `GET /api/gerencias/` - Listar gerencias
- `POST /api/gerencias/` - Crear gerencia
- `GET /api/gerencias/{id}/` - Detalle gerencia
- `PUT /api/gerencias/{id}/` - Actualizar gerencia
- `DELETE /api/gerencias/{id}/` - Eliminar gerencia

### Áreas
- `GET /api/areas/` - Listar áreas
- `POST /api/areas/` - Crear área
- `GET /api/areas/{id}/` - Detalle área

### Personal
- `GET /api/personal/` - Listar personal
- `GET /api/personal/activos/` - Personal activo
- `GET /api/personal/{id}/` - Detalle personal
- `GET /api/personal/{id}/roster/` - Roster del personal
- `POST /api/personal/` - Crear personal
- `PUT /api/personal/{id}/` - Actualizar personal

### Roster
- `GET /api/roster/` - Listar roster
- `GET /api/roster/por_rango/?fecha_desde=&fecha_hasta=` - Por rango
- `POST /api/roster/` - Crear registro
- `POST /api/roster/bulk_create/` - Creación masiva
- `PUT /api/roster/{id}/` - Actualizar registro

### Auditoría
- `GET /api/roster-audit/` - Historial de cambios

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov

# Tests específicos
pytest personal/tests/test_models.py

# Ver reporte HTML de coverage
pytest --cov --cov-report=html
open htmlcov/index.html
```

## 🔧 Comandos Útiles

### Django
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Datos de prueba
python manage.py seed_data --with-roster

# Shell
python manage.py shell

# Ejecutar tests
python manage.py test
```

### Celery
```bash
# Worker
celery -A config worker -l info

# Beat (tareas programadas)
celery -A config beat -l info

# Flower (monitor)
celery -A config flower
```

### Calidad de Código
```bash
# Ruff (linting y autofix)
ruff check . --fix

# Black (formatting)
black .

# isort (ordenar imports)
isort .

# Pre-commit (ejecutar hooks)
pre-commit run --all-files
```

## 🌐 Despliegue en Producción

### Heroku

```bash
# Crear app
heroku create mi-gestion-personal

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Agregar Redis
heroku addons:create heroku-redis:mini

# Variables de entorno
heroku config:set DJANGO_SECRET_KEY='tu-secret-key'
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production

# Deploy
git push heroku main

# Migraciones
heroku run python manage.py migrate

# Crear datos
heroku run python manage.py seed_data
```

### Railway / Render

Similar a Heroku, configurar:
- `DATABASE_URL` (PostgreSQL)
- `REDIS_URL` (Redis)
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn config.wsgi:application`

## 📝 Variables de Entorno

Ver `.env.example` para la lista completa. Principales:

```env
DJANGO_SECRET_KEY=tu-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tudominio.com
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
SENTRY_DSN=https://...
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 👤 Autor

Sistema desarrollado para gestión interna de personal.

## 📞 Soporte

Para soporte o consultas, contactar al equipo de desarrollo.
