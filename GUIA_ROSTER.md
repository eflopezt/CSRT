# Guía de Uso - Roster Matricial Editable

## Características Implementadas

### 1. Vista Matricial Editable
- **Edición inline**: Haz clic en cualquier celda de código para editarla directamente
- **Auto-guardado**: Los cambios se guardan automáticamente después de 1 segundo
- **Validación visual**:
  - 🟢 Verde: Códigos T y TR (generan días libres)
  - ⚪ Gris: Otros códigos (DL, V, DM, etc.) - no generan días libres
  - 🟡 Amarillo: Guardando...
  - 🟢 Verde claro: Guardado exitosamente
  - 🔴 Rojo: Error al guardar

### 2. Códigos del Roster

#### Códigos de Trabajo (generan días libres):
- **T**: Trabajo Presencial → Cada 3 días genera 1 día libre
- **TR**: Trabajo Remoto → Cada 5 días genera 2 días libres

#### Códigos de Descanso/Permisos:
- **DL**: Día Libre
- **DOL**: Compensación por Horario Extendido
- **DM**: Descanso Médico
- **V**: Vacaciones Aprobadas y/o Gozadas
- **F**: Feriado No Recuperable
- **FC**: Feriado Compensable

### 3. Cálculo Automático de Días Libres Ganados

La columna **"Días Libres Ganados"** se calcula automáticamente:

- **T (Trabajo Presencial)**: Por cada 3 días → 1 día libre
  - Ejemplo: 9 días con código "T" = 3 días libres ganados
  
- **TR (Trabajo Remoto)**: Por cada 5 días → 2 días libres
  - Ejemplo: 10 días con código "TR" = 4 días libres ganados
  
- **Total**: Suma de días libres de T + TR
  - Ejemplo: 9 T (3 libres) + 10 TR (4 libres) = **7 días libres ganados**

El cálculo se actualiza automáticamente cada vez que editas una celda.

### 4. Importación desde Excel

#### Formato del archivo:
```
| DNI      | Apellidos y Nombres | Día 01 | Día 02 | Día 03 | ... | Día 31 |
|----------|---------------------|--------|--------|--------|-----|--------|
| 12345678 | PEREZ LOPEZ JUAN    | T      | T      | T      | DL  | V      |
| 87654321 | GOMEZ DIAZ MARIA    | TR     | TR     | TR     | TR  | TR     |
```

#### Pasos para importar:
1. Ve a **Roster Matricial** → Botón **"Importar"**
2. Descarga la plantilla actual como referencia (opcional)
3. Selecciona tu archivo Excel
4. Haz clic en **"Importar"**
5. El sistema mostrará cuántos registros se crearon/actualizaron

⚠️ **Nota**: Si ya existen registros para las mismas fechas, serán actualizados.

### 5. Exportación a Excel

#### Desde Vista Matricial:
- Haz clic en el botón **"Exportar"**
- Se descargará un archivo Excel con:
  - Información del personal
  - Días Libres Ganados
  - Todos los códigos del mes
  - Días Trabajados calculados

#### Contenido del Excel exportado:
- **DNI**, **Apellidos y Nombres**, **Área**
- **Días Libres Ganados**: Valor acumulado del personal
- **Día 01** a **Día 31**: Códigos de cada día
- **Días Trabajados**: Cálculo automático

## Flujo de Trabajo Típico

### Opción A: Trabajo Manual
1. Ir a **Roster Matricial**
2. Seleccionar mes y año
3. Hacer clic en las celdas vacías
4. Escribir el código (T, TR, DL, V, etc.)
5. Presionar Enter o hacer clic fuera
6. El sistema guarda automáticamente y calcula días libres

### Opción B: Carga Masiva
1. Exportar el roster actual como plantilla
2. Abrir el Excel y completar/modificar los códigos
3. Guardar el archivo
4. Ir a **Importar Roster**
5. Subir el archivo
6. Verificar en la vista matricial

## Tips de Uso

### Navegación Rápida
- **Enter**: Guarda y pasa a la siguiente celda
- **Tab**: Navega entre celdas
- **Esc**: Cancela la edición (antes de guardar)

### Códigos de Trabajo
- Solo **T** y **TR** generan días libres
- "T1" o "TR2" NO generan días libres (deben ser exactamente T o TR)

### Filtros
- **Mes/Año**: Cambia el período visible
- **Área**: Filtra por área específica
- **Buscar**: Encuentra personal por DNI o nombre

### Impresión
- Usa el botón **"Imprimir"** para una versión optimizada
- Los filtros y botones no aparecen en la impresión

## Solución de Problemas

### La celda no se guarda
- Verifica tu conexión a internet
- Espera 1 segundo después de escribir
- La celda debe ponerse amarilla (guardando) y luego verde (guardado)

### Error al importar Excel
- Verifica que las columnas se llamen exactamente "DNI", "Día 01", "Día 02", etc.
- Asegúrate de que los DNIs existan en el sistema
- El personal debe estar previamente registrado

### Los días trabajados no se calculan bien
- Solo códigos numéricos (1, 2, 3) cuentan
- La fórmula es: (total numéricos) ÷ 3 redondeado
- Se recalcula automáticamente al editar

## Acceso Rápido

- **Vista Matricial**: `/roster/matricial/`
- **Importar**: `/roster/importar/`
- **Exportar**: `/roster/exportar/?mes=1&anio=2026`
- **API**: `/api/personal/`, `/api/roster/`

## Credenciales Admin
- **Usuario**: admin
- **Contraseña**: admin123
