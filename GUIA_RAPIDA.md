# ⚡ Guía Rápida de Uso

## 🚀 Inicio Rápido

### Verificar que todo está funcionando:
```bash
# Verificación automática
bash verificar_mejoras.sh

# Verificación manual
python manage.py check
python manage.py migrate --check
python manage.py shell < test_mejoras.py
```

---

## 📝 Uso de Validadores

### En modelos (automático):
```python
# Los modelos ya tienen validación automática en clean()
personal = Personal(nro_doc='12345678', tipo_doc='DNI')
personal.full_clean()  # Llama a clean() automáticamente
personal.save()
```

### En vistas (manual):
```python
from personal.validators import PersonalValidator

# Validar DNI
PersonalValidator.validar_nro_doc('12345678', 'DNI')

# Validar régimen de turno
dias_trabajo, dias_descanso = PersonalValidator.validar_regimen_turno('21x7')

# Validar monto
monto = PersonalValidator.validar_monto(1500.50, 'sueldo base', minimo=0.01)
```

---

## 🔄 Uso de Servicios Transaccionales

### Crear gerencia:
```python
from personal.services import GerenciaService

gerencia = GerenciaService.crear_gerencia(
    nombre="Operaciones",
    responsable=personal_obj,
    descripcion="Gerencia de Operaciones",
    usuario=request.user
)
```

### Actualizar roster:
```python
from personal.services import RosterService

roster = RosterService.actualizar_roster(
    roster_id=123,
    codigo='T',
    usuario=request.user,
    observaciones='Turno regular'
)
```

### Aprobar cambio:
```python
roster = RosterService.aprobar_cambio(
    roster_id=123,
    usuario=request.user
)
```

### Importar desde Excel:
```python
resultado = GerenciaService.importar_desde_excel(
    archivo=request.FILES['archivo'],
    usuario=request.user
)

print(f"Creados: {resultado['creados']}")
print(f"Actualizados: {resultado['actualizados']}")
print(f"Errores: {resultado['errores']}")
```

---

## 🛡️ Uso de Decoradores

### En vistas HTML:
```python
from personal.decorators import handle_exceptions, log_access

@login_required
@handle_exceptions(default_redirect='home')
@log_access('Creación de gerencia')
def crear_gerencia(request):
    # Tu código aquí
    # Errores se manejan automáticamente
    pass
```

### En APIs:
```python
from personal.decorators import handle_api_exceptions

@require_POST
@login_required
@handle_api_exceptions
def api_endpoint(request):
    # Tu código aquí
    # Errores retornan JSON automáticamente
    return JsonResponse({'success': True})
```

---

## 📊 Uso de Logging

### Logging básico:
```python
import logging

# En módulos de negocio
logger = logging.getLogger('personal.business')
logger.info("Operación exitosa")
logger.warning("Advertencia importante")
logger.error("Error crítico")

# En módulos de seguridad
security_logger = logging.getLogger('personal.security')
security_logger.warning(f"Acceso denegado: usuario {username}")
```

### Ver logs:
```bash
# Ver últimas 20 líneas del log general
tail -n 20 logs/general.log

# Ver errores
tail -f logs/errors.log

# Ver eventos de seguridad
tail -f logs/security.log

# Ver lógica de negocio
tail -f logs/business.log

# Buscar en logs
grep "ERROR" logs/*.log
```

---

## 🔍 Comandos Útiles

### Base de datos:
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations

# Ver SQL de una migración
python manage.py sqlmigrate personal 0007
```

### Testing:
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=personal

# Ejecutar prueba específica
pytest personal/tests/test_validators.py

# Ver reporte detallado
pytest -v
```

### Django shell:
```bash
# Shell interactivo
python manage.py shell

# Ejecutar script
python manage.py shell < test_mejoras.py
```

### Verificación:
```bash
# Verificar configuración
python manage.py check

# Verificar deploy
python manage.py check --deploy

# Ver settings activos
python manage.py diffsettings
```

---

## 📁 Estructura de Archivos Nuevos

```
/workspaces/CSRT/
│
├── config/
│   └── logging_config.py          # ← Configuración de logs
│
├── personal/
│   ├── validators.py               # ← Validadores centralizados
│   ├── services.py                 # ← Servicios transaccionales
│   ├── decorators.py               # ← Decoradores de excepciones
│   └── ejemplos_uso.py             # ← 7 ejemplos de uso
│
├── logs/                           # ← Directorio de logs
│   ├── general.log
│   ├── security.log
│   ├── business.log
│   └── errors.log
│
├── RESUMEN_MEJORAS.md              # ← Resumen ejecutivo
├── MEJORAS_IMPLEMENTADAS.md        # ← Guía completa
├── RECOMENDACIONES_FUTURO.md       # ← Próximas mejoras
├── GUIA_RAPIDA.md                  # ← Este archivo
├── test_mejoras.py                 # ← Script de pruebas
└── verificar_mejoras.sh            # ← Script de verificación
```

---

## 🎯 Flujo de Trabajo Recomendado

### 1. Al crear una nueva vista:
```python
from personal.decorators import handle_exceptions, log_access

@login_required
@handle_exceptions(default_redirect='lista')
@log_access('Descripción de la acción')
def mi_nueva_vista(request):
    # Tu código aquí
    pass
```

### 2. Al crear operaciones complejas:
```python
from django.db import transaction
from personal.services import MiServicio

# Usar servicio si existe
resultado = MiServicio.mi_operacion(datos, request.user)

# O crear transacción manual
with transaction.atomic():
    # Operaciones múltiples
    pass
```

### 3. Al validar datos:
```python
from personal.validators import MiValidator

# Validar antes de procesar
try:
    MiValidator.validar_dato(dato)
    # Procesar...
except ValidationError as e:
    messages.error(request, str(e))
```

### 4. Al hacer logging:
```python
import logging
logger = logging.getLogger('personal.business')

# Log al inicio
logger.info(f"Iniciando operación X para usuario {user}")

# Log de éxito
logger.info(f"Operación X completada exitosamente")

# Log de error
logger.error(f"Error en operación X: {str(e)}")
```

---

## 🐛 Debugging

### Ver logs en tiempo real:
```bash
# Terminal 1: Ejecutar servidor
python manage.py runserver

# Terminal 2: Ver logs
tail -f logs/general.log logs/errors.log
```

### Debug de validaciones:
```python
from personal.validators import PersonalValidator

try:
    PersonalValidator.validar_nro_doc('123', 'DNI')
except ValidationError as e:
    print(f"Error: {e.messages}")  # Lista de errores
```

### Debug de transacciones:
```python
from django.db import transaction
import logging

logger = logging.getLogger('personal.business')

with transaction.atomic():
    try:
        # Operaciones
        logger.info("Operación 1")
        # ...
        logger.info("Operación 2")
        # ...
    except Exception as e:
        logger.error(f"Error en transacción: {str(e)}")
        # La transacción se revierte automáticamente
        raise
```

---

## ⚡ Mejores Prácticas

### ✅ DO (Hacer):
- Usar decoradores en todas las vistas
- Usar servicios para operaciones complejas
- Validar datos antes de procesar
- Hacer logging de operaciones importantes
- Usar transacciones para operaciones múltiples
- Leer logs regularmente

### ❌ DON'T (No hacer):
- Usar `except:` sin especificar excepción
- Ignorar errores de validación
- Hacer operaciones complejas sin transacciones
- Olvidar hacer logging de seguridad
- Repetir validaciones en múltiples lugares

---

## 📚 Referencias Rápidas

### Documentación completa:
- [RESUMEN_MEJORAS.md](RESUMEN_MEJORAS.md) - Resumen ejecutivo
- [MEJORAS_IMPLEMENTADAS.md](MEJORAS_IMPLEMENTADAS.md) - Guía detallada
- [RECOMENDACIONES_FUTURO.md](RECOMENDACIONES_FUTURO.md) - Próximas mejoras

### Ejemplos:
- [personal/ejemplos_uso.py](personal/ejemplos_uso.py) - 7 ejemplos completos

### Scripts:
- `bash verificar_mejoras.sh` - Verificación automática
- `python manage.py shell < test_mejoras.py` - Pruebas

---

## 🆘 Solución de Problemas

### "Archivo no encontrado: logs/general.log"
```bash
mkdir -p logs
chmod 755 logs
```

### "ImportError: cannot import name 'LOGGING'"
```python
# En config/settings/base.py verificar:
from config.logging_config import LOGGING
```

### "ValidationError no se maneja"
```python
# Agregar decorador:
from personal.decorators import handle_exceptions

@handle_exceptions(default_redirect='home')
def mi_vista(request):
    pass
```

### "Logs no se escriben"
```python
# Verificar configuración de logging en settings
from django.conf import settings
print(settings.LOGGING)
```

---

## 🎉 ¡Listo para Usar!

Ahora puedes:
1. ✅ Crear vistas robustas con decoradores
2. ✅ Validar datos con validadores centralizados
3. ✅ Ejecutar operaciones transaccionales seguras
4. ✅ Monitorear el sistema con logs estructurados
5. ✅ Mantener la facilidad de inicio de sesión

**¿Dudas?** Consulta los archivos de documentación o revisa los ejemplos en `personal/ejemplos_uso.py`
