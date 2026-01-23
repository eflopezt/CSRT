# Instrucciones para Deploy Manual en Render

## 📋 Resumen de Cambios

**Commit**: `0c71e30` - fix: Preservar ceros a la izquierda en campo DNI

### Cambios Implementados:
- ✅ Corrección de importación de DNI preservando ceros a la izquierda
- ✅ Formato de texto en exportaciones Excel
- ✅ Procesamiento robusto de valores numéricos
- ✅ Nueva herramienta `corregir_dni.py`
- ✅ Documentación completa

### Archivos Modificados:
- `personal/views.py` - Importación con dtype str
- `personal/excel_utils.py` - Formato de texto en columnas DNI
- `corregir_dni.py` - Nueva herramienta (no se ejecuta en producción)
- `docs/CORRECCION_DNI.md` - Documentación
- `.gitignore` - Excluir backups/

## 🚀 Pasos para Deploy Manual en Render

### Opción 1: Deploy Automático desde GitHub (Recomendado)

Si tienes configurado el auto-deploy en Render:

1. Ve a tu dashboard de Render: https://dashboard.render.com
2. Selecciona tu servicio `CSRT` (o el nombre que le hayas dado)
3. Render detectará automáticamente el nuevo commit
4. El deploy se iniciará automáticamente
5. Espera a que termine (verás "Live" en verde)

### Opción 2: Deploy Manual desde Dashboard

Si el auto-deploy está desactivado:

1. Ve a tu dashboard de Render: https://dashboard.render.com
2. Selecciona tu servicio
3. Haz clic en el botón **"Manual Deploy"** (arriba a la derecha)
4. Selecciona la rama: **main**
5. Haz clic en **"Deploy"**
6. Espera a que termine el deploy

### Opción 3: Deploy desde Línea de Comandos

Si tienes configurado el CLI de Render:

```bash
# Instalar Render CLI (si no lo tienes)
npm install -g @render/cli

# Login
render login

# Deploy
render deploy --service <tu-service-id>
```

## 🔍 Verificación Post-Deploy

### 1. Verificar que el Servicio Está Live

```
Dashboard → Tu Servicio → Estado: "Live" (verde)
```

### 2. Revisar Logs

```
Dashboard → Tu Servicio → Logs
```

Busca mensajes como:
```
Starting service with 'gunicorn config.wsgi:application'
Booting worker with pid: ...
```

### 3. Probar Funcionalidades Clave

Accede a tu aplicación en producción y verifica:

- [ ] Login funciona
- [ ] Exportación de plantilla Personal descarga correctamente
- [ ] Importación de Excel con DNI mantiene ceros (prueba con DNI tipo `00123456`)
- [ ] Las vistas principales cargan sin errores

### 4. Verificar DNIs en Producción (Opcional)

Si quieres verificar que no hay DNIs con problemas en producción:

```bash
# Conectarse por SSH a Render (si tienes acceso)
# O ejecutar desde el dashboard si tienes shell habilitado

python corregir_dni.py --listar
```

## ⚠️ Migraciones

Este deploy **NO incluye migraciones nuevas** porque solo se modificó lógica de negocio.

La última migración aplicada es: `0008_rename_models_area_subarea`

Si en el futuro hay migraciones nuevas, Render las aplicará automáticamente durante el deploy.

## 🔄 Rollback (Si algo sale mal)

### Opción 1: Rollback desde Dashboard

1. Ve a Render Dashboard
2. Selecciona tu servicio
3. Ve a la pestaña **"Deploys"**
4. Encuentra el deploy anterior (commit `dd43ece`)
5. Haz clic en **"Redeploy"**

### Opción 2: Rollback desde Git

```bash
# Revertir el commit
git revert 0c71e30

# Push
git push origin main

# Render detectará el cambio y hará redeploy
```

## 📊 Monitoreo Post-Deploy

### Primeros 15 minutos:

- ✅ Revisar logs en busca de errores
- ✅ Verificar métricas de memoria/CPU (no deberían cambiar)
- ✅ Probar importación de Excel

### Primera hora:

- ✅ Monitorear errores en logs
- ✅ Verificar que usuarios pueden trabajar normalmente

### Primeras 24 horas:

- ✅ Revisar si hay reportes de usuarios sobre DNIs
- ✅ Verificar que las importaciones funcionan correctamente

## 📝 Notas Importantes

### Impacto en Producción

- **Nivel de Riesgo**: BAJO ⚠️
- **Downtime Esperado**: ~30-60 segundos durante deploy
- **Cambios en BD**: Ninguno
- **Reversible**: Sí, fácilmente

### Compatibilidad

- ✅ Compatible con datos existentes
- ✅ No requiere cambios en BD
- ✅ No afecta funcionalidad existente
- ✅ Solo mejora el manejo de DNIs en importaciones futuras

### Archivos de Backup

Se creó un backup local en:
```
backups/backup_20260123_114348/
├── db.sqlite3
├── migrations_personal/
└── README.txt
```

**Nota**: Este backup es solo para desarrollo local, no afecta producción.

## 🆘 Soporte

Si encuentras problemas después del deploy:

1. **Revisa los logs en Render**
2. **Verifica el estado del servicio**
3. **Si hay errores críticos, haz rollback**
4. **Revisa la documentación**: `docs/CORRECCION_DNI.md`

## ✅ Checklist de Deploy

Antes de marcar como completado:

- [ ] Backup creado localmente
- [ ] Cambios commiteados a Git
- [ ] Push a GitHub exitoso
- [ ] Deploy en Render iniciado
- [ ] Deploy completado (estado "Live")
- [ ] Logs sin errores críticos
- [ ] Funcionalidad básica verificada
- [ ] Importación de Excel probada (opcional)

---

**Fecha**: 2026-01-23  
**Commit**: 0c71e30  
**Estado**: ✅ Listo para deploy
