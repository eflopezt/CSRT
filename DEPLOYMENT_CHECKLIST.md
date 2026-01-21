# 🚀 Checklist de Despliegue - Sistema de Gestión Personal

## ✅ Revisión Pre-Despliegue Completada

### 1. Modelos y Base de Datos
- ✅ Modelos correctamente definidos con validaciones
- ✅ Índices de base de datos para campos frecuentes (nro_doc, fecha, personal)
- ✅ unique_together en Roster (personal, fecha) y Area (nombre, gerencia)
- ✅ Relaciones ForeignKey con on_delete apropiados
- ✅ Validadores MinValue en campos numéricos

### 2. Seguridad
- ✅ Todas las vistas protegidas con @login_required
- ✅ Sistema de permisos basado en roles (Admin/Responsable)
- ✅ Filtrado de datos según usuario (solo ve su gerencia)
- ✅ SECRET_KEY validación en producción (no permite default)
- ✅ Configuraciones de seguridad en production.py:
  - SECURE_SSL_REDIRECT = True
  - SESSION_COOKIE_SECURE = True
  - CSRF_COOKIE_SECURE = True
  - X_FRAME_OPTIONS = 'DENY'
- ✅ CSRF tokens en todos los formularios
- ⚠️ **IMPORTANTE**: Cambiar SECRET_KEY antes de desplegar

### 3. Manejo de Errores
- ✅ Try-catch con excepciones específicas (ValueError, TypeError, InvalidOperation)
- ✅ Mensajes informativos al usuario (success, error, warning, info)
- ✅ Validación de datos en importación Excel
- ✅ Logging configurado para producción

### 4. Importación/Exportación Excel
- ✅ Validaciones de columnas requeridas
- ✅ Manejo de datos faltantes con pd.notna()
- ✅ Conversión de tipos con try-catch
- ✅ Plantillas con catálogos y listas desplegables
- ✅ Opción de plantilla vacía para todos los módulos
- ✅ Feedback detallado (registros creados/actualizados/errores)

### 5. Cálculos de Días Libres
- ✅ Lógica correcta para régimen de turno (21x7, 15x3, etc.)
- ✅ TR siempre es 5x2
- ✅ Acumulación decimal y redondeo al final
- ✅ Días pendientes = (corte 2025 + ganados) - usados

### 6. Configuración de Producción
- ✅ Settings modulares (base/development/production)
- ✅ DEBUG = False en producción
- ✅ ALLOWED_HOSTS desde variable de entorno
- ✅ PostgreSQL configurado con DATABASE_URL
- ✅ WhiteNoise para archivos estáticos
- ✅ .env.example con todas las variables necesarias
- ✅ .gitignore configurado correctamente

### 7. URLs y Templates
- ✅ Todas las rutas definidas en urls.py
- ✅ Nombres de URL consistentes
- ✅ Enlaces correctos en templates
- ✅ Botones Export/Import en todos los módulos
- ✅ Paginación implementada en listados

## ⚠️ Acciones Requeridas Antes de Desplegar

### Variables de Entorno (Obligatorias)
```bash
# Generar nueva SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar en servidor:
export DJANGO_SECRET_KEY="tu-clave-super-secreta-aqui"
export DJANGO_ALLOWED_HOSTS="tudominio.com,www.tudominio.com"
export DJANGO_SETTINGS_MODULE="config.settings.production"
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
export CSRF_TRUSTED_ORIGINS="https://tudominio.com,https://www.tudominio.com"
```

### Base de Datos
```bash
# En producción, ejecutar:
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input

# Opcional: Cargar datos iniciales
python manage.py seed_data
python manage.py create_responsables_users
```

### Servidor Web
- Configurar Gunicorn/uWSGI
- Nginx como proxy reverso
- HTTPS con Let's Encrypt/Certbot
- Configurar archivos estáticos en /staticfiles/

### Monitoreo (Opcional pero Recomendado)
- Configurar Sentry DSN para tracking de errores
- Logs en /logs/ (crear directorio)
- Backup automático de base de datos

## 🐛 Problemas Conocidos Resueltos

1. ✅ HTTP 405 en logout → Creada vista personalizada
2. ✅ Campos financieros removidos del formulario Personal
3. ✅ Gerencia se obtiene automáticamente del área (no manual)
4. ✅ except genéricos → especificados (ValueError, TypeError, etc.)
5. ✅ Plantillas vacías disponibles para importación

## 📝 Datos de Prueba

### Usuarios Creados
- **Admin**: admin / admin123 (acceso completo)
- **Responsables**: 
  - jgarcia / responsable123 (Gerencia Operaciones)
  - mrodriguez / responsable123 (Gerencia Mantenimiento)
  - pfernandez / responsable123 (Gerencia Logística)
  - amartinez / responsable123 (Gerencia Administración)

### Datos Iniciales
- 4 Gerencias
- 6 Áreas
- 8 Personal de ejemplo

## 🔒 Recomendaciones de Seguridad

1. **Cambiar todas las contraseñas de prueba** en producción
2. Habilitar autenticación de dos factores (si aplica)
3. Limitar intentos de login (django-axes)
4. Backup regular de base de datos
5. Revisar logs periódicamente
6. Mantener dependencias actualizadas
7. Usar PostgreSQL (no SQLite) en producción

## 📊 Rendimiento

- Queries optimizadas con select_related() y prefetch_related()
- Índices de base de datos en campos frecuentes
- Paginación en listados largos
- WhiteNoise para servir estáticos eficientemente

## 🎯 Funcionalidades Principales Verificadas

1. ✅ **Gerencias**: CRUD + Export/Import Excel
2. ✅ **Áreas**: CRUD + Export/Import Excel
3. ✅ **Personal**: CRUD + Export/Import Excel + Vista detalle
4. ✅ **Roster**: 
   - CRUD individual
   - Vista matricial (calendario)
   - Export/Import Excel
   - Edición en línea
   - Cálculo automático de días libres

## 📱 Compatibilidad

- ✅ Responsive design con Bootstrap 5
- ✅ Compatible con navegadores modernos
- ✅ Mobile-friendly

## 🚀 Comandos de Despliegue

```bash
# 1. Clonar repositorio
git clone https://github.com/eflopezt/CSRT.git
cd CSRT

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con valores de producción

# 5. Migraciones y datos iniciales
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input

# 6. Iniciar servidor (desarrollo)
python manage.py runserver

# 6. Iniciar servidor (producción)
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## ✅ Estado Final

**El sistema está listo para despliegue** con todas las funcionalidades implementadas y probadas.

Se recomienda hacer un despliegue en ambiente de staging primero para pruebas finales antes de producción.

---
**Fecha de revisión**: 21 de Enero de 2026
**Revisado por**: GitHub Copilot
