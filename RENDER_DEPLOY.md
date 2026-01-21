# 🚀 Guía de Despliegue en Render

## Paso 1: Crear Base de Datos PostgreSQL en Render

1. Ve a [https://dashboard.render.com/](https://dashboard.render.com/)
2. Clic en **"New +"** → **"PostgreSQL"**
3. Configuración:
   - **Name**: `csrt-database` (o el nombre que prefieras)
   - **Database**: `csrt_db`
   - **User**: (se genera automáticamente)
   - **Region**: Elige la más cercana a tus usuarios
   - **PostgreSQL Version**: 16 (o la más reciente)
   - **Plan**: Elige según tu necesidad
     - **Free**: Para pruebas (expira en 90 días)
     - **Starter**: $7/mes (recomendado para producción)

4. Clic en **"Create Database"**
5. **IMPORTANTE**: Guarda las siguientes credenciales (las necesitarás):
   - **Internal Database URL** (para usar dentro de Render)
   - **External Database URL** (para acceso externo)

### Formato de las URLs:
```
Internal: postgresql://user:password@hostname-internal:5432/database
External: postgresql://user:password@hostname-external:5432/database
```

---

## Paso 2: Crear Web Service en Render

1. En el Dashboard de Render, clic en **"New +"** → **"Web Service"**

2. **Conectar tu repositorio**:
   - Selecciona **"Connect a repository"**
   - Autoriza Render a acceder a tu GitHub
   - Busca y selecciona: `eflopezt/CSRT`

3. **Configuración básica**:
   - **Name**: `csrt-app` (o el nombre que prefieras)
   - **Region**: La misma que la base de datos
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

4. **Seleccionar Plan**:
   - **Free**: Para pruebas (el servicio se apaga después de inactividad)
   - **Starter**: $7/mes (recomendado - siempre activo)

---

## Paso 3: Configurar Variables de Entorno

En la configuración del Web Service, ve a la sección **"Environment"** y agrega:

### Variables Obligatorias:

```bash
# Django Core
DJANGO_SECRET_KEY=
# Genera una nueva con: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

DJANGO_SETTINGS_MODULE=config.settings.production

# Hosts permitidos (usa el dominio de Render)
DJANGO_ALLOWED_HOSTS=csrt-app.onrender.com,csrt-app-XXXXX.onrender.com
# Reemplaza con tu URL real de Render

# Base de datos (copia la Internal Database URL de tu PostgreSQL)
DATABASE_URL=postgresql://user:password@hostname-internal:5432/csrt_db

# CSRF (usa tu dominio de Render con https)
CSRF_TRUSTED_ORIGINS=https://csrt-app.onrender.com
```

### Variables Opcionales:

```bash
# Sentry para monitoreo de errores (opcional)
SENTRY_DSN=

# Email (si necesitas enviar correos)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-app

# Redis (si usas Celery - requiere crear servicio Redis aparte)
REDIS_URL=redis://hostname:6379/0
CELERY_BROKER_URL=redis://hostname:6379/0
CELERY_RESULT_BACKEND=redis://hostname:6379/0

# CORS (solo si tienes frontend separado)
CORS_ALLOWED_ORIGINS=https://tu-frontend.com
```

---

## Paso 4: Generar SECRET_KEY Segura

En tu terminal local, ejecuta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en la variable `DJANGO_SECRET_KEY` en Render.

---

## Paso 5: Desplegar

1. Revisa que todas las variables estén configuradas
2. Clic en **"Create Web Service"**
3. Render automáticamente:
   - Clona tu repositorio
   - Ejecuta `build.sh` (instala dependencias, collectstatic, migrate)
   - Inicia la aplicación con Gunicorn

### Monitorear el Despliegue:

En el dashboard verás:
- **Logs**: Para ver el progreso del build
- **Events**: Historial de despliegues
- **Shell**: Para ejecutar comandos en el servidor

---

## Paso 6: Crear Superusuario

Una vez desplegado, necesitas crear un usuario admin:

1. Ve a tu servicio en Render
2. Clic en **"Shell"** (en el menú lateral)
3. Ejecuta:

```bash
python manage.py createsuperuser
```

4. Ingresa:
   - **Username**: admin (o el que prefieras)
   - **Email**: tu-email@ejemplo.com
   - **Password**: (contraseña segura)

---

## Paso 7: Cargar Datos Iniciales (Opcional)

Si quieres cargar los datos de ejemplo:

```bash
# En el Shell de Render:
python manage.py seed_data
python manage.py create_responsables_users
```

---

## Paso 8: Acceder a tu Aplicación

Tu aplicación estará disponible en:
```
https://csrt-app.onrender.com
```
(Reemplaza con tu URL real)

### Usuarios de prueba (si cargaste datos):
- **Admin**: admin / (la contraseña que creaste)
- **Responsables**: jgarcia, mrodriguez, etc. / responsable123

---

## 🔧 Comandos Útiles en Render Shell

```bash
# Ver migraciones
python manage.py showmigrations

# Aplicar migraciones específicas
python manage.py migrate personal

# Colectar archivos estáticos manualmente
python manage.py collectstatic --no-input

# Ver logs de Django
tail -f logs/django.log

# Abrir shell de Django
python manage.py shell

# Listar usuarios
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.all())"
```

---

## 🔄 Actualizaciones y Re-despliegues

Cada vez que hagas `git push` a la rama `main`, Render automáticamente:
1. Detecta los cambios
2. Ejecuta `build.sh`
3. Re-inicia la aplicación

### Despliegue Manual:
1. Ve a tu servicio en Render
2. Clic en **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🐛 Troubleshooting

### Error: "relation does not exist"
```bash
# En Shell de Render:
python manage.py migrate --run-syncdb
```

### Error: "SECRET_KEY must be set"
- Verifica que `DJANGO_SECRET_KEY` esté en las variables de entorno
- No debe estar vacía ni ser la clave por defecto

### Error: "ALLOWED_HOSTS"
- Agrega todos los dominios de Render a `DJANGO_ALLOWED_HOSTS`
- Formato: `dominio1.onrender.com,dominio2.onrender.com`

### La aplicación no carga estáticos:
```bash
# En Shell de Render:
python manage.py collectstatic --no-input --clear
```

### Ver logs en tiempo real:
- Ve a **"Logs"** en el dashboard de Render
- Los errores aparecerán aquí

---

## 📊 Monitoreo y Mantenimiento

### Backup de Base de Datos:
1. Ve a tu PostgreSQL en Render
2. Clic en **"Backups"**
3. Render hace backups automáticos (en planes pagos)

### Backup Manual:
```bash
# Desde tu computadora local (usando External Database URL):
pg_dump -h hostname-external -U user -d csrt_db -F c -f backup_$(date +%Y%m%d).dump
```

### Restaurar Backup:
```bash
pg_restore -h hostname-external -U user -d csrt_db backup_20260121.dump
```

---

## 💰 Costos Estimados

### Plan Gratuito (Free):
- **Web Service**: Gratis (se suspende tras inactividad)
- **PostgreSQL**: Gratis por 90 días, luego expira
- **Limitaciones**: Suspensión automática, datos temporales

### Plan de Producción (Recomendado):
- **Web Service Starter**: $7/mes
- **PostgreSQL Starter**: $7/mes (1GB RAM, 10GB storage)
- **Total**: ~$14/mes

---

## 🔐 Seguridad en Producción

### Cambiar contraseñas de prueba:
```bash
# En Shell de Render:
python manage.py changepassword admin
python manage.py changepassword jgarcia
# etc...
```

### Habilitar HTTPS (automático en Render):
- Render proporciona certificado SSL gratis
- Todas las conexiones son HTTPS por defecto

### Variables de entorno sensibles:
- Nunca las subas a Git
- Usa solo las variables de entorno de Render

---

## 📱 Dominio Personalizado (Opcional)

1. Ve a tu Web Service en Render
2. Clic en **"Settings"** → **"Custom Domains"**
3. Agrega tu dominio: `www.tudominio.com`
4. Configura DNS en tu proveedor:
   ```
   CNAME www tudominio.onrender.com
   ```
5. Actualiza `DJANGO_ALLOWED_HOSTS`:
   ```
   DJANGO_ALLOWED_HOSTS=www.tudominio.com,tudominio.com,csrt-app.onrender.com
   ```

---

## ✅ Checklist Final

- [ ] Base de datos PostgreSQL creada
- [ ] Variables de entorno configuradas
- [ ] SECRET_KEY generada y agregada
- [ ] ALLOWED_HOSTS con dominio de Render
- [ ] DATABASE_URL (Internal) configurada
- [ ] Servicio web creado y desplegado
- [ ] Superusuario creado
- [ ] Aplicación accesible vía HTTPS
- [ ] Contraseñas de prueba cambiadas
- [ ] Backup configurado

---

## 🆘 Soporte

- **Documentación Render**: https://render.com/docs
- **Community Forum**: https://community.render.com
- **Status**: https://status.render.com

---

¡Tu aplicación está lista para producción en Render! 🎉
