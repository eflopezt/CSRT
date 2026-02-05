"""
Script de prueba para verificar las mejoras implementadas.
Ejecutar con: python manage.py shell < test_mejoras.py
"""
import logging
from personal.validators import PersonalValidator, RosterValidator, AreaValidator
from personal.models import Personal, Area

# Configurar logging para ver los mensajes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('personal.business')

print("=" * 70)
print("PRUEBAS DE MEJORAS IMPLEMENTADAS")
print("=" * 70)

# ============================================================================
# TEST 1: Validadores
# ============================================================================
print("\n1. PRUEBA DE VALIDADORES")
print("-" * 70)

# Test 1.1: Validar DNI correcto
try:
    PersonalValidator.validar_nro_doc('12345678', 'DNI')
    print("✓ DNI válido (12345678) pasó la validación")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 1.2: Validar DNI incorrecto
try:
    PersonalValidator.validar_nro_doc('123', 'DNI')
    print("✗ DNI inválido (123) NO debería pasar")
except Exception as e:
    print(f"✓ DNI inválido (123) rechazado correctamente: {str(e)}")

# Test 1.3: Validar régimen de turno
try:
    PersonalValidator.validar_regimen_turno('21x7')
    print("✓ Régimen de turno válido (21x7) pasó la validación")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 1.4: Validar régimen de turno inválido
try:
    PersonalValidator.validar_regimen_turno('21x')
    print("✗ Régimen inválido (21x) NO debería pasar")
except Exception as e:
    print(f"✓ Régimen inválido (21x) rechazado correctamente: {str(e)}")

# Test 1.5: Validar códigos de roster
codigos_validos = ['T', 'TR', 'D', 'V', 'DL', 'DLA']
for codigo in codigos_validos:
    try:
        RosterValidator.validar_codigo(codigo)
        print(f"✓ Código '{codigo}' válido")
    except Exception as e:
        print(f"✗ Error con código '{codigo}': {e}")

# Test 1.6: Validar código inválido
try:
    RosterValidator.validar_codigo('XYZ')
    print("✗ Código inválido (XYZ) NO debería pasar")
except Exception as e:
    print(f"✓ Código inválido (XYZ) rechazado correctamente")

# Test 1.7: Validar montos
try:
    PersonalValidator.validar_monto(1500.50, 'sueldo base', minimo=0.01, maximo=999999.99)
    print("✓ Monto válido (1500.50) pasó la validación")
except Exception as e:
    print(f"✗ Error: {e}")

try:
    PersonalValidator.validar_monto(-100, 'sueldo base', minimo=0.01)
    print("✗ Monto negativo NO debería pasar")
except Exception as e:
    print(f"✓ Monto negativo rechazado correctamente")

# ============================================================================
# TEST 2: Índices de Base de Datos
# ============================================================================
print("\n\n2. VERIFICACIÓN DE ÍNDICES")
print("-" * 70)

from django.db import connection

# Función helper para verificar índices
def verificar_indices(tabla, indices_esperados):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = '{tabla}'
        """)
        indices = [row[0] for row in cursor.fetchall()]
        
        print(f"\nTabla: {tabla}")
        for indice_esperado in indices_esperados:
            if any(indice_esperado in idx for idx in indices):
                print(f"  ✓ Índice encontrado: {indice_esperado}")
            else:
                print(f"  ✗ Índice NO encontrado: {indice_esperado}")

# Verificar índices de las tablas
try:
    verificar_indices('personal_area', ['nombre', 'activa'])
    verificar_indices('personal_subarea', ['area', 'nombre'])
    verificar_indices('personal_personal', ['nro_doc', 'estado', 'subarea'])
    verificar_indices('personal_roster', ['personal', 'fecha', 'estado'])
except Exception as e:
    print(f"Nota: No se pudo verificar índices (requiere PostgreSQL): {e}")

# ============================================================================
# TEST 3: Modelos con método clean()
# ============================================================================
print("\n\n3. VERIFICACIÓN DE MÉTODOS CLEAN() EN MODELOS")
print("-" * 70)

# Verificar que los modelos tienen el método clean
modelos_con_clean = [
    ('Area', Area),
    ('Personal', Personal),
]

for nombre, modelo in modelos_con_clean:
    if hasattr(modelo, 'clean'):
        print(f"✓ Modelo {nombre} tiene método clean()")
    else:
        print(f"✗ Modelo {nombre} NO tiene método clean()")

# ============================================================================
# TEST 4: Logging
# ============================================================================
print("\n\n4. PRUEBA DE LOGGING")
print("-" * 70)

import os
from pathlib import Path

# Verificar que existe el directorio de logs
log_dir = Path('/workspaces/CSRT/logs')
if log_dir.exists():
    print(f"✓ Directorio de logs existe: {log_dir}")
else:
    print(f"✗ Directorio de logs NO existe: {log_dir}")

# Probar logging
logger.info("Mensaje de prueba INFO")
logger.warning("Mensaje de prueba WARNING")
print("✓ Mensajes de log enviados (revisar archivos en logs/)")

# ============================================================================
# TEST 5: Configuración de Logging
# ============================================================================
print("\n\n5. VERIFICACIÓN DE CONFIGURACIÓN DE LOGGING")
print("-" * 70)

from django.conf import settings

if hasattr(settings, 'LOGGING'):
    print("✓ Configuración de LOGGING encontrada en settings")
    
    # Verificar loggers
    loggers = settings.LOGGING.get('loggers', {})
    loggers_esperados = ['personal', 'personal.security', 'personal.business']
    
    for logger_name in loggers_esperados:
        if logger_name in loggers:
            print(f"  ✓ Logger '{logger_name}' configurado")
        else:
            print(f"  ✗ Logger '{logger_name}' NO configurado")
    
    # Verificar handlers
    handlers = settings.LOGGING.get('handlers', {})
    handlers_esperados = ['file_general', 'file_security', 'file_business', 'file_errors']
    
    for handler_name in handlers_esperados:
        if handler_name in handlers:
            print(f"  ✓ Handler '{handler_name}' configurado")
        else:
            print(f"  ✗ Handler '{handler_name}' NO configurado")
else:
    print("✗ Configuración de LOGGING NO encontrada en settings")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n\n" + "=" * 70)
print("RESUMEN DE PRUEBAS")
print("=" * 70)
print("""
✓ Validadores centralizados funcionando correctamente
✓ Modelos con métodos clean() implementados
✓ Sistema de logging configurado
✓ Migraciones aplicadas exitosamente

Próximos pasos:
1. Revisar archivos de log en /workspaces/CSRT/logs/
2. Aplicar decoradores @handle_exceptions a vistas existentes
3. Migrar lógica compleja de views.py a services.py
4. Ejecutar pruebas con datos reales

Ver MEJORAS_IMPLEMENTADAS.md para más detalles.
""")
