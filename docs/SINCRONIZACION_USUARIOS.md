# Sincronización Automática de Usuarios

Esta funcionalidad automatiza la creación y vinculación de usuarios del sistema con los registros de Personal.

## 🎯 Propósito

Facilitar la administración de usuarios eliminando la necesidad de crear y vincular usuarios manualmente uno por uno.

## 🚀 Métodos de Uso

### 1. **Interfaz Web (Recomendado)**

Acceder desde el menú de administración:

```
Panel Admin → Usuarios → Botón "Sincronizar Usuarios"
```

O directamente en: `https://tu-dominio.com/usuarios/sincronizar/`

**Características:**
- ✅ Interfaz visual intuitiva
- ✅ Estadísticas en tiempo real
- ✅ Vista previa de usuarios creados
- ✅ Exportación de credenciales

### 2. **Comando de Terminal**

Para administradores que prefieren la línea de comandos o automatización:

```bash
# Ver todas las opciones
python manage.py sincronizar_usuarios --help

# Vincular usuarios existentes Y crear faltantes (recomendado)
python manage.py sincronizar_usuarios

# Solo vincular usuarios existentes
python manage.py sincronizar_usuarios --vincular-existentes

# Solo crear nuevos usuarios
python manage.py sincronizar_usuarios --crear-usuarios

# Con contraseña personalizada (por defecto es DNI)
python manage.py sincronizar_usuarios --password-default "MiPassword123"

# Solo personal activo
python manage.py sincronizar_usuarios --solo-activos

# Modo simulación (ver qué haría sin hacer cambios)
python manage.py sincronizar_usuarios --dry-run
```

## 📋 ¿Qué hace la sincronización?

### **Vincular Usuarios Existentes**
- Busca usuarios cuyo `username` coincida con el DNI del personal
- Verifica que el usuario no esté ya vinculado a otro personal
- Crea la vinculación automáticamente

### **Crear Usuarios Nuevos**
- Identifica personal sin usuario asignado (que tenga DNI)
- Crea un usuario con:
  - **Username:** Primera letra del nombre + Apellido paterno (ej: Juan Pérez López → jperez)
  - **Email:** Correo corporativo o personal del registro
  - **Password:** El número de DNI
  - **Nombre:** Extraído del campo `apellidos_nombres`
- Vincula automáticamente el usuario al personal
- Si el personal es responsable de área, lo agrega al grupo correspondiente
- Si el username ya existe, agrega un número secuencial (jperez1, jperez2, etc.)

## ⚙️ Requisitos

Para que un registro de Personal pueda tener usuario creado:
- ✅ Debe tener **tipo de documento = DNI**
- ✅ Debe tener número de DNI registrado
- ✅ El DNI no debe estar duplicado
- ✅ No debe existir ya un usuario con ese DNI como username

## 📊 Ejemplo de Uso

**Escenario:** Tienes 50 personas en el sistema, 10 tienen usuario y 40 no.

```bash
# Ejecutar sincronización
python manage.py sincronizar_usuarios --solo-activos

# Resultado:
✅ Personal ya vinculado: 10
🔗 Usuarios vinculados: 5    # Usuarios existentes que se vincularon
👤 Usuarios creados: 35       # Nuevos usuarios creados
⚠️  Personal sin DNI: 0
❌ Errores: 0
```

## 🔐 Seguridad

**Formato de credenciales:**
- **Username:** Primera letra del nombre + Apellido paterno (ej: Juan Pérez → `jperez`)
- **Password:** El número de DNI del personal

⚠️ **IMPORTANTE:**
- Los usuarios **DEBEN** cambiar su contraseña en el primer acceso
- Considera implementar política de cambio obligatorio de contraseña
- Notifica a los usuarios sus credenciales de manera segura
- El DNI como contraseña inicial es fácil de recordar pero debe cambiarse

**Ventajas de este formato:**
- Username corto y fácil de recordar
- Password es información que el personal ya conoce (su DNI)
- Facilita la comunicación de credenciales iniciales

## 📝 Recomendaciones

1. **Antes de iniciar producción:**
   ```bash
   # Simular primero para ver qué hará
   python manage.py sincronizar_usuarios --dry-run
   ```

2. **Backup antes de sincronización masiva:**
   ```bash
   python manage.py dumpdata auth.User personal.Personal > backup_pre_sync.json
   ```

3. **Ejecutar fuera de horario pico:**
   - Preferentemente en horario de mantenimiento
   - Cuando no haya usuarios activos en el sistema

4. **Documentar credenciales:**
   - Exportar lista de usuarios creados desde la interfaz web
   - Enviar credenciales por canal seguro

## 🆘 Solución de Problemas

### Error: "Ya existe usuario con ese username"
**Causa:** Ya existe un usuario con ese username generado (ej: jperez)
**Solución:** El sistema agregará automáticamente un número (jperez1, jperez2, etc.)

### Error: "Formato de nombre inválido"
**Causa:** El registro no tiene al menos apellido y nombre
**Solución:** Actualizar registro con formato: Apellido_Paterno Apellido_Materno Nombres

### Error: "Personal sin DNI"
**Causa:** El registro no tiene DNI o no es tipo DNI
**Solución:** Actualizar registro con DNI válido

### Usuario creado pero no puede acceder
**Verificar:**
1. Usuario está activo (`is_active=True`)
2. Contraseña es correcta
3. No hay restricciones de IP/red

## 📚 Documentación Adicional

- Ver: `personal/management/commands/sincronizar_usuarios.py` para detalles de implementación
- Ver: `personal/views.py` función `usuario_sincronizar` para lógica web

## 🔄 Automatización Futura

Para automatizar completamente (ejemplo: nuevo personal → usuario automático):

1. Usar **Django Signals** en `personal/signals.py`
2. Agregar al post_save de Personal
3. Crear usuario automáticamente si cumple requisitos

---

**Desarrollado para:** Sistema de Gestión de Personal  
**Versión:** 1.0  
**Fecha:** Enero 2026
