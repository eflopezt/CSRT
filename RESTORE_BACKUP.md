# 🔄 INSTRUCCIONES PARA RESTAURAR BACKUP

## Información del Backup
- **Fecha de creación**: 2026-01-22 13:54:21
- **Commit hash**: a90dab1
- **Tag de Git**: backup-estable-20260122-135421

---

## ⚠️ OPCIÓN 1: Restaurar usando Git (RECOMENDADO)

Este método mantiene el historial de git y es el más limpio.

```bash
cd /workspaces/CSRT

# Descartar todos los cambios no confirmados
git reset --hard

# Volver al punto de backup usando el tag
git reset --hard backup-estable-20260122-135421

# O alternativamente, usar el commit hash
git reset --hard a90dab1

# Verificar que todo esté correcto
python manage.py check
```

---

## 📦 OPCIÓN 2: Restaurar desde archivo comprimido

Si necesitas restaurar todo desde cero:

```bash
# Ir al directorio padre
cd /workspaces

# Hacer backup del estado actual (por si acaso)
mv CSRT CSRT-pre-restore-$(date '+%Y%m%d-%H%M%S')

# Extraer el backup
tar -xzf backup-csrt-20260122-135431.tar.gz
mv CSRT-backup CSRT  # Ajustar nombre según sea necesario

cd CSRT

# Restaurar la base de datos
cp ../backup-db-20260122-135441.sqlite3 ./db.sqlite3

# Verificar
python manage.py check
```

---

## 🗄️ OPCIÓN 3: Restaurar solo la base de datos

Si solo quieres restaurar la base de datos:

```bash
cd /workspaces/CSRT

# Hacer backup de la DB actual
cp db.sqlite3 db.sqlite3.pre-restore

# Restaurar la DB del backup
cp ../backup-db-20260122-135441.sqlite3 ./db.sqlite3

# Verificar
python manage.py migrate --check
```

---

## ✅ Verificación Post-Restauración

Después de restaurar, ejecuta estos comandos para verificar que todo funcione:

```bash
cd /workspaces/CSRT

# 1. Verificar la configuración de Django
python manage.py check

# 2. Verificar las migraciones
python manage.py showmigrations

# 3. Ejecutar las pruebas de validación (si existen)
python test_validations.py

# 4. Iniciar el servidor de desarrollo (opcional)
python manage.py runserver
```

---

## 📝 Archivos de Backup Disponibles

- **Código completo**: `/workspaces/backup-csrt-20260122-135431.tar.gz`
- **Base de datos**: `/workspaces/backup-db-20260122-135441.sqlite3`
- **Commit Git**: `a90dab1`
- **Tag Git**: `backup-estable-20260122-135421`

---

## 🆘 En caso de problemas

Si algo sale mal durante la restauración:

```bash
# Ver el estado actual de git
git status
git log --oneline -10

# Ver todos los tags disponibles
git tag -l "backup-*"

# Listar todos los backups en archivos
ls -lh /workspaces/backup-*
```
