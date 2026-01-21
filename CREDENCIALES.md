# Credenciales de Acceso - Sistema de Gestión de Personal

## Administrador del Sistema

- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Acceso total a todo el sistema

---

## Responsables de Gerencia

Los responsables de gerencia solo pueden ver y gestionar el personal y áreas bajo su gerencia.

### GERENCIA DE OPERACIONES
- **Responsable:** GARCÍA LÓPEZ, JUAN CARLOS
- **Usuario:** `jgarcia`
- **Contraseña:** `responsable123`
- **Permisos:**
  - Ver y editar personal de su gerencia
  - Ver áreas de su gerencia
  - Gestionar roster de su personal

### GERENCIA DE LOGÍSTICA
- **Responsable:** RODRÍGUEZ PÉREZ, MARÍA ELENA
- **Usuario:** `mrodriguez`
- **Contraseña:** `responsable123`
- **Permisos:**
  - Ver y editar personal de su gerencia
  - Ver áreas de su gerencia
  - Gestionar roster de su personal

### GERENCIA DE RECURSOS HUMANOS
- **Responsable:** FERNÁNDEZ TORRES, PEDRO LUIS
- **Usuario:** `pfernandez`
- **Contraseña:** `responsable123`
- **Permisos:**
  - Ver y editar personal de su gerencia
  - Ver áreas de su gerencia
  - Gestionar roster de su personal

### GERENCIA DE FINANZAS
- **Responsable:** MARTÍNEZ SÁNCHEZ, ANA SOFÍA
- **Usuario:** `amartinez`
- **Contraseña:** `responsable123`
- **Permisos:**
  - Ver y editar personal de su gerencia
  - Ver áreas de su gerencia
  - Gestionar roster de su personal

---

## Características del Sistema de Permisos

### Para Administradores (Superusuarios)
- ✅ Acceso completo a todas las gerencias
- ✅ Ver y editar todo el personal
- ✅ Crear y editar gerencias y áreas
- ✅ Gestionar todo el roster
- ✅ Acceso al panel de administración de Django

### Para Responsables de Gerencia
- ✅ Ver solo su gerencia
- ✅ Ver solo las áreas de su gerencia
- ✅ Ver y editar solo personal asignado a áreas de su gerencia
- ✅ Gestionar roster solo de su personal
- ❌ No pueden ver ni editar personal de otras gerencias
- ❌ No pueden crear o editar gerencias
- ⚠️ Al editar personal, solo pueden asignarlos a áreas de su propia gerencia

### Validaciones Automáticas
- Los filtros se aplican automáticamente en todas las vistas
- Los responsables no pueden acceder a datos de otras gerencias mediante URL directa
- Las actualizaciones del roster validan permisos antes de guardar
- El sistema muestra un badge identificando el rol del usuario

---

## Notas de Seguridad

1. **Cambiar contraseñas:** Se recomienda que cada usuario cambie su contraseña al primer acceso
2. **Contraseñas temporales:** Todas las contraseñas `responsable123` son temporales
3. **Grupos de Django:** El sistema usa el grupo "Responsable de Gerencia" para gestionar permisos

---

## Cómo Crear Nuevos Usuarios

Si se asigna un nuevo responsable a una gerencia:

```bash
python manage.py create_responsables_users
```

Este comando:
- Detecta automáticamente gerencias con responsables
- Crea usuarios si no existen
- Asigna los permisos correspondientes
- Vincula el usuario con el personal

---

## URL del Sistema

**Desarrollo:** http://localhost:8000

**Login:** http://localhost:8000/login/
