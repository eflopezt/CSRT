# 🚀 QUICK START - Render Deployment

## 📋 Pre-requisitos
- [ ] Cuenta en Render.com
- [ ] Código subido a GitHub (eflopezt/CSRT)
- [ ] SECRET_KEY generada

---

## 🎯 Pasos Rápidos (5 minutos)

### 1️⃣ Crear PostgreSQL (2 min)
```
Render Dashboard → New + → PostgreSQL
Name: csrt-database
Plan: Starter ($7/mes)
```
**➡️ Copia el "Internal Database URL"**

### 2️⃣ Crear Web Service (2 min)
```
Render Dashboard → New + → Web Service
Repository: eflopezt/CSRT
Name: csrt-app
Build: ./build.sh
Start: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
Plan: Starter ($7/mes)
```

### 3️⃣ Variables de Entorno (1 min)
**Mínimo necesario:**
```bash
DJANGO_SECRET_KEY=<genera-uno-nuevo>
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_ALLOWED_HOSTS=csrt-app.onrender.com
DATABASE_URL=<pega-internal-url-del-paso-1>
CSRF_TRUSTED_ORIGINS=https://csrt-app.onrender.com
```

### 4️⃣ Deploy
Clic en **"Create Web Service"** → Espera 3-5 minutos

### 5️⃣ Crear Superuser
```bash
Render Dashboard → tu servicio → Shell
python manage.py createsuperuser
```

---

## ✅ URLs Finales

- **App**: https://csrt-app.onrender.com
- **Admin**: https://csrt-app.onrender.com/admin
- **Dashboard Render**: https://dashboard.render.com

---

## 🔑 Generar SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 💰 Costo Total
- PostgreSQL Starter: $7/mes
- Web Service Starter: $7/mes
- **Total: $14/mes**

*(Plan Free disponible para pruebas)*

---

## 📖 Documentación Completa
Ver: [RENDER_DEPLOY.md](RENDER_DEPLOY.md)
