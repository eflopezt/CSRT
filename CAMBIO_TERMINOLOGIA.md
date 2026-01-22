# Cambio de Terminología: Gerencia → Área, Área → SubÁrea

## Resumen de Cambios

Se ha realizado un cambio completo de terminología en el sistema:

### 1. Cambios en Modelos

**ANTES:**
- `Gerencia`: Departamentos de alto nivel (1 responsable)
- `Area`: Áreas bajo gerencias
- `Personal.area`: ForeignKey a Area

**DESPUÉS:**
- `Area`: Áreas o departamentos de alto nivel (1 responsable)
- `SubArea`: SubÁreas bajo áreas
- `Personal.subarea`: ForeignKey a SubArea

### 2. Archivos Modificados

#### Modelos y Lógica de Negocio
- ✅ [personal/models.py](personal/models.py) - Renombrado de clases y relaciones
- ✅ [personal/admin.py](personal/admin.py) - Actualizado registro de admin
- ✅ [personal/forms.py](personal/forms.py) - Formularios actualizados
- ✅ [personal/serializers.py](personal/serializers.py) - Serializers API REST
- ✅ [personal/validators.py](personal/validators.py) - Validadores
- ✅ [personal/permissions.py](personal/permissions.py) - Permisos y filtros
- ✅ [personal/services.py](personal/services.py) - Servicios de negocio

#### Vistas y URLs
- ✅ [personal/views.py](personal/views.py) - Todas las vistas actualizadas
- ✅ [personal/urls.py](personal/urls.py) - URLs actualizadas
- ✅ [personal/api_views.py](personal/api_views.py) - ViewSets API
- ✅ [personal/api_urls.py](personal/api_urls.py) - URLs API

#### Utilidades
- ✅ [personal/excel_utils.py](personal/excel_utils.py) - Exportación/importación Excel

#### Templates
- ✅ Renombrados:
  - `gerencia_list.html` → `area_list.html`
  - `gerencia_form.html` → `area_form.html`
  - `area_list.html` → `subarea_list.html`
  - `area_form.html` → `subarea_form.html`
  
- ✅ Actualizados (contenido):
  - `personal_list.html`
  - `personal_detail.html`
  - `roster_matricial.html`
  - `dashboard_aprobaciones.html`
  - `import_form.html`
  - Y otros...

### 3. Cambios en la Base de Datos

Se generó la migración: `0008_rename_models_area_subarea.py`

**Operaciones de la migración:**
1. Crea modelo `SubArea`
2. Elimina campo `responsable` de `Gerencia` (antiguo)
3. Modifica opciones Meta de `Area`
4. Elimina índices obsoletos
5. Elimina campo `area` de `Personal`
6. Agrega campo `responsable` a `Area` (nuevo)
7. Modifica campo `nombre` en `Area`
8. Agrega campo `area` a `SubArea`
9. Agrega campo `subarea` a `Personal`
10. Crea nuevos índices
11. **Elimina modelo `Gerencia`**

### 4. URLs Actualizadas

**ANTES:**
```
/gerencias/
/gerencias/crear/
/gerencias/<id>/editar/
/areas/
/areas/crear/
/areas/<id>/editar/
```

**DESPUÉS:**
```
/areas/
/areas/crear/
/areas/<id>/editar/
/subareas/
/subareas/crear/
/subareas/<id>/editar/
```

### 5. API Endpoints

**ANTES:**
```
api/gerencias/
api/areas/
```

**DESPUÉS:**
```
api/areas/
api/subareas/
```

### 6. Funciones y Permisos

**ANTES:**
- `get_gerencia_responsable(user)`
- `es_responsable_gerencia(user)`
- `filtrar_gerencias(user)`
- `filtrar_areas(user)`

**DESPUÉS:**
- `get_area_responsable(user)`
- `es_responsable_area(user)`
- `filtrar_areas(user)`
- `filtrar_subareas(user)`

### 7. Variables de Contexto

En views y templates, las variables fueron actualizadas:
- `gerencia` → `area` / `area_resp`
- `gerencias` → `areas`
- `area` → `subarea`
- `areas` → `subareas`

### 8. Textos Visibles (UI)

Todos los textos visibles en la interfaz fueron actualizados:
- "Gerencia" → "Área"
- "Gerencias" → "Áreas"
- "Área" → "SubÁrea"
- "Áreas" → "SubÁreas"

### 9. Configuración del Proyecto

Actualizado [.github/copilot-instructions.md](.github/copilot-instructions.md) con la nueva estructura.

## Scripts Utilizados

Se crearon scripts temporales para facilitar el cambio masivo:
1. `rename_area_to_subarea.py` - Cambió Area → SubArea en Python
2. `update_templates_area_to_subarea.py` - Cambió Area → SubArea en templates
3. `rename_gerencia_to_area.py` - Cambió Gerencia → Area en Python
4. `update_templates_gerencia_to_area.py` - Cambió Gerencia → Area en templates
5. `fix_final_references.py` - Correcciones finales
6. `fix_all_gerencia_refs.py` - Últimas correcciones

## Próximos Pasos

### ⚠️ IMPORTANTE: Antes de ejecutar en producción

1. **Hacer backup completo de la base de datos**
2. **Revisar la migración generada** en `personal/migrations/0008_rename_models_area_subarea.py`
3. **Ejecutar la migración en desarrollo primero**:
   ```bash
   python manage.py migrate personal
   ```
4. **Verificar que todo funcione correctamente**
5. **Actualizar datos existentes** si es necesario
6. **Ejecutar pruebas**
7. **Desplegar en producción**

### Comandos para aplicar cambios

```bash
# 1. Verificar migraciones pendientes
python manage.py showmigrations personal

# 2. Aplicar migración
python manage.py migrate personal

# 3. Verificar estado
python manage.py check
```

## Verificación del Sistema

✅ **Sintaxis Python**: Todos los archivos compilan sin errores
✅ **Django Check**: Sistema pasa todas las verificaciones
✅ **Migraciones**: Generadas correctamente
✅ **URLs**: Actualizadas y funcionando
✅ **Templates**: Renombrados y actualizados
✅ **API**: Endpoints actualizados

## Notas Importantes

- Los cambios son **retrocompatibles** a nivel de código, pero **NO a nivel de base de datos**
- La migración eliminará la tabla `Gerencia` y creará/modificará tablas según la nueva estructura
- Todos los datos existentes deben ser migrados cuidadosamente
- Se recomienda hacer un backup antes de aplicar la migración en producción
- Los permisos de usuario pueden necesitar actualización ("Responsable de Gerencia" → "Responsable de Área")
