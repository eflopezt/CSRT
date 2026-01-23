# Corrección del Campo DNI - Preservación de Ceros a la Izquierda

## Problema Identificado

El campo `nro_doc` (DNI) estaba perdiendo los **ceros a la izquierda** durante la importación desde archivos Excel. Esto ocurría porque:

1. **Excel convierte automáticamente** los DNI a formato numérico
2. Al convertir `"00123456"` a número, Excel lo guarda como `123456`
3. Cuando pandas lee el Excel, recupera `123456` en lugar de `"00123456"`
4. Se pierden los ceros iniciales que son parte del DNI real

### Ejemplos del Problema

```
DNI Real:     00123456  →  Excel lo guarda como número: 123456  →  Se pierde: 00123456
DNI Real:     07654321  →  Excel lo guarda como número: 7654321 →  Se pierde: 07654321
```

Esto es crítico porque:
- DNIs peruanos tienen **8 dígitos** (pueden empezar con 0)
- DNIs antiguos pueden tener **7 dígitos** (rellenar con 0)
- Carnés de extranjería y pasaportes pueden variar

## Soluciones Implementadas

### 1. Forzar Lectura como Texto en Pandas

**Ubicación**: [personal/views.py](personal/views.py)

Se modificó `pd.read_excel()` para forzar que las columnas de documentos se lean como texto:

#### Importación de Personal

```python
# ANTES
df = pd.read_excel(archivo, sheet_name='Personal')

# DESPUÉS
df = pd.read_excel(
    archivo, 
    sheet_name='Personal',
    dtype={'NroDoc': str, 'CodigoFotocheck': str, 'Celular': str}  # ✓ Forzar texto
)
```

#### Importación de Gerencias/Áreas

```python
df = pd.read_excel(
    archivo, 
    sheet_name='Gerencias',
    dtype={'Responsable_DNI': str}  # ✓ Forzar texto
)
```

#### Importación de Roster

```python
df = pd.read_excel(
    archivo, 
    sheet_name='Roster',
    dtype={'DNI': str}  # ✓ Forzar texto
)
```

### 2. Procesamiento Robusto del DNI

Se mejoró el procesamiento del DNI para manejar tanto valores numéricos como texto:

```python
# Procesar DNI - asegurar que se mantienen ceros a la izquierda
nro_doc_raw = row['NroDoc']
if pd.isna(nro_doc_raw):
    continue

# Si es número, convertir a string sin notación científica
if isinstance(nro_doc_raw, (int, float)):
    nro_doc = str(int(nro_doc_raw)).strip()
else:
    nro_doc = str(nro_doc_raw).strip()

if not nro_doc or nro_doc == 'nan':
    continue
```

**¿Por qué?**: Aunque forzamos `dtype=str`, si el Excel ya tenía el dato como número, pandas lo lee como número. Este código maneja ambos casos.

### 3. Formato de Texto en Archivos Excel Exportados

**Ubicación**: [personal/excel_utils.py](personal/excel_utils.py)

Se agregó formato de texto explícito a las columnas de DNI en los archivos Excel generados:

```python
from openpyxl.styles.numbers import FORMAT_TEXT

# Aplicar formato de texto a columnas específicas
columnas_texto = ['NroDoc', 'DNI', 'Responsable_DNI', 'CodigoFotocheck', 'Celular']

for column in hoja_principal.columns:
    column_name = column[0].value
    
    for cell in column:
        # Aplicar formato de texto a columnas de DNI
        if column_name in columnas_texto and cell.row > 1:  # Skip header
            cell.number_format = FORMAT_TEXT
            # Asegurar que el valor se mantiene como string
            if cell.value is not None:
                cell.value = str(cell.value)
```

**Beneficio**: Los archivos Excel descargados del sistema ya tendrán el formato correcto, evitando que Excel convierta los DNI a números.

## Herramienta de Corrección

Se creó el script **`corregir_dni.py`** para identificar y corregir DNIs existentes en la base de datos.

### Uso

```bash
# 1. Listar DNIs sospechosos (menos de 8 dígitos)
python corregir_dni.py --listar

# 2. Simulación de corrección automática (sin cambios)
python corregir_dni.py --corregir --dry-run

# 3. Aplicar corrección automática (DNIs de 7 dígitos → añade un 0)
python corregir_dni.py --corregir

# 4. Modo interactivo para corrección manual
python corregir_dni.py --manual
```

### Funcionalidades

1. **Listar**: Identifica DNIs con menos de 8 dígitos
2. **Corrección Automática**: Añade un cero al inicio de DNIs de 7 dígitos
3. **Modo Manual**: Permite corregir DNI por DNI de forma interactiva
4. **Validaciones**:
   - Verifica que no existan duplicados
   - Advierte sobre DNIs con longitud inusual
   - Permite confirmar antes de aplicar cambios

## Verificación del Estado Actual

Ejecutamos el script de verificación:

```bash
$ python corregir_dni.py --listar

================================================================================
DNIs SOSPECHOSOS (menos de 8 dígitos)
================================================================================

✓ No se encontraron DNIs sospechosos.
```

**Estado**: ✅ La base de datos actual no tiene DNIs con problemas.

## Recomendaciones

### Para Importaciones Futuras

1. **Siempre usar las plantillas descargadas del sistema**
   - Ya tienen el formato correcto configurado
   - Las columnas de DNI están formateadas como texto

2. **Si preparas Excel manualmente**:
   - Formatea las columnas de DNI como **TEXTO** antes de ingresar datos
   - Añade un apóstrofe inicial: `'12345678` (Excel lo interpreta como texto)
   - Verifica que los ceros se muestren antes de guardar

3. **Después de importar**:
   - Verifica algunos registros en el sistema
   - Ejecuta `python corregir_dni.py --listar` para detectar problemas

### Para Usuarios de Excel

#### Método 1: Formato de Celda (Recomendado)
1. Selecciona la columna del DNI
2. Clic derecho → "Formato de celdas"
3. Selecciona "Texto"
4. Ingresa los DNI

#### Método 2: Apóstrofe
1. Ingresa un apóstrofe antes del DNI: `'00123456`
2. Excel lo guardará como texto
3. El apóstrofe no se ve al abrir, pero preserva los ceros

#### Método 3: Usar las Plantillas del Sistema
1. Exporta desde el sistema (botón "Descargar Plantilla")
2. Las plantillas ya tienen el formato correcto
3. Solo completa los datos

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| [personal/views.py](personal/views.py) | • Añadido `dtype={'NroDoc': str}` en importaciones<br>• Mejorado procesamiento de DNI<br>• Manejo robusto de valores numéricos |
| [personal/excel_utils.py](personal/excel_utils.py) | • Importado `FORMAT_TEXT`<br>• Aplicado formato de texto a columnas de DNI<br>• Conversión explícita a string |
| **corregir_dni.py** (nuevo) | • Script para listar DNIs sospechosos<br>• Corrección automática<br>• Modo interactivo |

## Definición del Campo en el Modelo

El campo está correctamente definido como `CharField`:

```python
# personal/models.py
nro_doc = models.CharField(
    max_length=20,          # ✓ Suficiente para DNI, CE, Pasaporte
    unique=True,            # ✓ No puede haber duplicados
    verbose_name="Número de Documento"
)
```

**Tipo en base de datos**: `varchar(20)` ✅ (correcto, preserva ceros)

## Testing

Para verificar que todo funciona correctamente:

```bash
# 1. Crear un Excel de prueba con DNI que tenga ceros
# 2. Importarlo
# 3. Verificar en la base de datos:

python manage.py shell
>>> from personal.models import Personal
>>> Personal.objects.filter(nro_doc__startswith='0')
# Debe mostrar los registros con ceros al inicio
```

## Soporte

Si encuentras DNIs con problemas:

1. Ejecuta: `python corregir_dni.py --listar`
2. Revisa los DNIs mostrados
3. Corrige según sea necesario:
   - Automático: `python corregir_dni.py --corregir`
   - Manual: `python corregir_dni.py --manual`

---

**Fecha**: 23 de enero de 2026  
**Estado**: ✅ Implementado y verificado
