# Validación de Días Libres Pendientes

## Resumen de Cambios

Se ha implementado una validación para evitar que los "Días Libres Pendientes" sean negativos cuando se intenta usar el código "DL" en el roster.

## Archivos Modificados

### 1. `/workspaces/CSRT/personal/models.py`

**Nuevo método agregado al modelo `Personal`:**

```python
def validar_saldo_dl(self, nuevo_dl=False):
    """
    Valida que los días libres pendientes no sean negativos después de usar DL.
    Retorna (es_valido, mensaje, dias_pendientes)
    """
```

Este método:
- Calcula los días libres ganados, días DL usados y días DLA usados
- Si `nuevo_dl=True`, simula agregar un DL adicional
- Calcula los días libres pendientes considerando:
  - Saldo al 31/12/25 (después de descontar DLA)
  - Días libres ganados
  - Días DL usados
- Retorna `False` si los días pendientes serían negativos con el mensaje: "No tiene más días libres pendientes disponibles"

### 2. `/workspaces/CSRT/personal/views.py`

**Modificaciones en la vista `roster_update_cell`:**

Se agregó validación para el código 'DL' (líneas ~1148-1156):

```python
# Validaciones especiales para DL
if codigo == 'DL':
    # Validar que haya días libres pendientes disponibles
    es_valido_dl, mensaje_dl, dias_pendientes = personal.validar_saldo_dl(nuevo_dl=True)
    if not es_valido_dl:
        return JsonResponse({
            'success': False,
            'error': f'No se puede usar DL. {mensaje_dl}',
            'revert': True,
            'old_value': codigo_anterior
        }, status=400)
```

**Modificaciones en la vista `roster_import`:**

Se agregó validación en la importación de Excel (líneas ~1030-1038):

```python
# Validaciones especiales para DL
if codigo == 'DL':
    # Validar que haya días libres pendientes disponibles
    es_valido_dl, mensaje_dl, dias_pendientes = personal.validar_saldo_dl(nuevo_dl=True)
    if not es_valido_dl:
        errores.append(f"Fila {idx + 2}, Día {dia}: {mensaje_dl}")
        continue
```

## Funcionamiento

1. **Actualización manual en roster matricial**: Cuando un usuario intenta ingresar "DL" en una celda del roster, se valida automáticamente si tiene días libres pendientes disponibles. Si no tiene, se muestra un error y la celda se revierte al valor anterior.

2. **Importación desde Excel**: Durante la importación de rosters desde Excel, si se intenta importar un "DL" para un personal que no tiene días disponibles, se registra un error y se omite ese registro.

3. **Mensaje de error**: El mensaje muestra claramente: "No tiene más días libres pendientes disponibles. Días libres pendientes actuales: X"

## Cálculo de Días Libres Pendientes

La fórmula utilizada es:

```
Días Libres Pendientes = (Días al 31/12/25 - DLA usados) + Días Ganados - DL usados
```

Donde:
- **Días al 31/12/25**: Saldo de días acumulados al corte
- **DLA usados**: Días Libres Acumulados que descuentan del saldo del corte
- **Días Ganados**: Días libres ganados durante el año actual basados en turnos T y TR
- **DL usados**: Días Libres utilizados que descuentan de los días disponibles

## Pruebas Realizadas

Se creó el script `test_dl_validation.py` que verifica:

✅ Validación del estado actual de días libres
✅ Validación al intentar usar un nuevo DL
✅ Simulación de alcanzar el límite de días disponibles
✅ Caso con personal que no tiene días disponibles (validación correcta)

## Comportamiento Esperado

- ✅ Si el personal tiene días libres pendientes > 0, puede usar DL
- ❌ Si el personal tiene días libres pendientes = 0, NO puede usar DL
- ❌ Si usar un DL haría que los días pendientes sean negativos, se bloquea la operación

## Integración

Esta validación se integra perfectamente con las validaciones existentes de DLA:
- DLA valida contra el saldo al 31/12/25 (no puede ser negativo)
- DLA valida máximo 7 días consecutivos
- DL valida contra días libres pendientes totales (no puede ser negativo)
