# 📋 Sistema de Aprobaciones de Roster - Documentación

## ✅ Características Implementadas

### 1. **Roles y Permisos**

#### 👤 Personal Regular
- ✅ **Ver**: Solo su propio roster
- ✅ **Editar**: Solo su propio roster (día actual en adelante)
- ✅ **Restricción**: No puede editar días anteriores
- ✅ **Restricción**: No puede editar antes de enero 2026
- ✅ **Estado**: Los cambios quedan en `borrador` hasta enviarlos

#### 👔 Líder de Gerencia/Área
- ✅ **Ver**: Roster de todo su equipo (área/gerencia a cargo)
- ✅ **Editar**: Roster de su equipo (día actual en adelante)
- ✅ **Aprobar**: Cambios pendientes de su equipo
- ✅ **Estado**: Sus cambios quedan `aprobados` inmediatamente
- ✅ **Dashboard**: Ve cambios pendientes en el inicio

#### 👑 Administrador
- ✅ **Ver**: Todo el sistema
- ✅ **Editar**: Todo, incluyendo días anteriores
- ✅ **Aprobar**: Todos los cambios pendientes
- ✅ **Sin restricciones**: Puede editar antes de 2026

---

### 2. **Sistema de Estados**

Los registros de roster tienen 3 estados:

| Estado | Descripción | Quién lo genera |
|--------|-------------|-----------------|
| `borrador` | Cambio sin enviar | Personal regular |
| `pendiente` | Enviado para aprobación | Al enviar borrador |
| `aprobado` | Cambio confirmado | Líder/Admin |

---

### 3. **Flujo de Trabajo**

#### Para Personal Regular:
1. Editar su roster en la vista matricial
2. Los cambios quedan en `borrador` (fondo amarillo claro)
3. Aparece mensaje: "Tiene cambios sin enviar"
4. Click en **"Enviar Cambios para Aprobación"**
5. Los cambios pasan a estado `pendiente`
6. Esperar aprobación del líder

#### Para Líderes:
1. Ver notificación en el inicio: "X cambios pendientes"
2. Click en **"Ver Cambios"** o ir a `/roster/cambios-pendientes/`
3. Revisar lista de cambios pendientes
4. **Aprobar** ✅ o **Rechazar** ❌ cada cambio
5. Los aprobados pasan a `aprobado`
6. Los rechazados se eliminan

---

### 4. **Nuevas Vistas y URLs**

| URL | Vista | Descripción |
|-----|-------|-------------|
| `/roster/cambios-pendientes/` | `cambios_pendientes` | Lista de cambios pendientes |
| `/roster/aprobar/<pk>/` | `aprobar_cambio` | Aprobar un cambio (POST) |
| `/roster/rechazar/<pk>/` | `rechazar_cambio` | Rechazar un cambio (POST) |
| `/roster/enviar-aprobacion/` | `enviar_cambios_aprobacion` | Enviar borradores (POST) |

---

### 5. **Campos Agregados al Modelo Roster**

```python
estado = CharField  # 'borrador', 'pendiente', 'aprobado'
modificado_por = ForeignKey(User)  # Quién hizo el cambio
aprobado_por = ForeignKey(User)    # Quién aprobó
aprobado_en = DateTimeField        # Cuándo se aprobó
```

---

### 6. **Validaciones Implementadas**

✅ **Fecha límite enero 2026**: No se puede editar antes de 2026
✅ **Fecha actual**: Solo admin puede editar días anteriores
✅ **Permisos de personal**: Solo se edita propio roster o de equipo
✅ **DLA consecutivos**: Máximo 7 días consecutivos
✅ **Saldo DLA**: No puede quedar negativo al 31/12/25

---

### 7. **Interfaz de Usuario**

#### Home / Inicio
- Nuevo contador: "Cambios Pendientes"
- Alerta destacada cuando hay cambios por aprobar
- Botón rápido para ir a ver cambios

#### Vista Matricial del Roster
- Los cambios en `borrador` se muestran con fondo especial
- Botón flotante: "Enviar Cambios para Aprobación"
- Contador de cambios sin enviar

#### Vista de Cambios Pendientes
- Tabla con todos los cambios pendientes
- Información completa: fecha, personal, código, quién modificó
- Botones de acción: Aprobar ✅ / Rechazar ❌
- Actualización AJAX sin recargar página

---

### 8. **Métodos del Modelo Roster**

```python
def puede_editar(self, usuario):
    """Verifica si un usuario puede editar este registro."""
    # Retorna (bool, mensaje_error)

def puede_aprobar(self, usuario):
    """Verifica si un usuario puede aprobar este cambio."""
    # Retorna bool
```

---

## 🚀 Para Empezar a Usar

### 1. Aplicar Migraciones
Ya aplicadas automáticamente:
- `0006_roster_aprobado_en_roster_aprobado_por_roster_estado_and_more`

### 2. Verificar Sistema
```bash
python manage.py check
```

### 3. Iniciar Servidor
```bash
python manage.py runserver
```

---

## 📝 Notas Importantes

1. **Retrocompatibilidad**: Los registros existentes se marcan como `aprobado` por defecto

2. **Admin siempre tiene acceso total**: Puede editar cualquier fecha, cualquier personal

3. **Los borradores son privados**: Solo el usuario que los crea puede verlos hasta enviarlos

4. **Rechazar elimina el registro**: No se guarda historial de cambios rechazados

5. **Los líderes aprueban inmediatamente**: Sus cambios no requieren aprobación

---

## 🔐 Seguridad

- ✅ Decoradores `@login_required` en todas las vistas
- ✅ Validación de permisos en cada operación
- ✅ CSRF protection en formularios AJAX
- ✅ Verificación de propiedad de registros
- ✅ Logs de auditoría (modelo RosterAudit existente)

---

## 🎨 Mejoras Futuras Sugeridas

1. **Notificaciones**: Email cuando haya cambios pendientes
2. **Historial**: Ver cambios rechazados en auditoría
3. **Comentarios**: Agregar razón al rechazar
4. **Bulk actions**: Aprobar/rechazar múltiples cambios
5. **Filtros**: Por área, fecha, personal en cambios pendientes
6. **Dashboard**: Gráficos de aprobaciones por período

---

## 🐛 Solución de Problemas

### "No tiene permisos para editar"
- Verificar que el usuario tenga perfil Personal asignado
- Verificar que sea líder de la gerencia/área correcta
- Verificar que la fecha sea >= hoy (excepto admin)

### "No se puede editar antes de enero 2026"
- Solo el admin puede modificar datos anteriores a 2026
- Los demás usan el campo `dias_libres_corte_2025`

### Cambios no aparecen
- Verificar el estado del registro
- Los `borrador` solo los ve el creador
- Los `pendiente` solo los ven los aprobadores

---

**Sistema listo para producción** ✅

Fecha de implementación: 22 de enero de 2026
