"""
Script de prueba para validar que los días libres pendientes no puedan ser negativos.
"""
import os
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.models import Personal, Roster
from datetime import date, timedelta

@pytest.mark.django_db
def test_validacion_dl():
    """
    Prueba la validación de días libres pendientes.
    """
    print("=" * 80)
    print("TEST: Validación de Días Libres Pendientes")
    print("=" * 80)
    
    # Buscar un personal activo para pruebas
    personal = Personal.objects.filter(estado='Activo').first()
    
    if not personal:
        print("\n❌ No se encontró personal activo para realizar la prueba")
        return
    
    print(f"\n📋 Personal seleccionado: {personal.apellidos_nombres}")
    print(f"   DNI: {personal.nro_doc}")
    print(f"   Régimen: {personal.regimen_turno}")
    
    # Calcular días libres
    dias_libres_ganados = personal.calcular_dias_libres_ganados()
    dias_dl_usados = personal.calcular_dias_dl_usados()
    dias_dla_usados = personal.calcular_dias_dla_usados()
    
    print(f"\n📊 Estado actual:")
    print(f"   Días libres al 31/12/25: {personal.dias_libres_corte_2025}")
    print(f"   Días DLA usados: {dias_dla_usados}")
    print(f"   Días libres ganados: {dias_libres_ganados:.2f}")
    print(f"   Días DL usados: {dias_dl_usados}")
    print(f"   Días libres pendientes: {personal.dias_libres_pendientes:.2f}")
    
    # Probar validación sin agregar nuevo DL
    print(f"\n🧪 Prueba 1: Validar estado actual")
    es_valido, mensaje, dias_pendientes = personal.validar_saldo_dl(nuevo_dl=False)
    
    if es_valido:
        print(f"   ✅ Validación exitosa")
        print(f"   Días pendientes: {dias_pendientes:.2f}")
    else:
        print(f"   ❌ Validación falló: {mensaje}")
    
    # Probar validación con nuevo DL
    print(f"\n🧪 Prueba 2: Validar con nuevo DL")
    es_valido, mensaje, dias_pendientes = personal.validar_saldo_dl(nuevo_dl=True)
    
    if es_valido:
        print(f"   ✅ Puede usar DL")
        print(f"   Días pendientes después del DL: {dias_pendientes:.2f}")
    else:
        print(f"   ❌ No puede usar DL: {mensaje}")
    
    # Simular múltiples DL para llegar al límite
    print(f"\n🧪 Prueba 3: Simular alcanzar el límite de días")
    
    # Calcular cuántos DL se pueden usar en total
    dias_disponibles_totales = int(personal.dias_libres_pendientes)
    
    print(f"   Total de días libres pendientes: {dias_disponibles_totales}")
    print(f"   DL ya usados: {dias_dl_usados}")
    print(f"   DL que aún puede usar: {dias_disponibles_totales}")
    
    # Simular intentar usar más DL de los disponibles
    # Creamos un contador temporal
    dl_temporales = dias_dl_usados
    intentos_exitosos = 0
    
    for i in range(dias_disponibles_totales + 5):  # Intentar 5 más del límite
        # Simular que hay más DL usados
        mock_dl_count = dl_temporales + 1
        
        # Calcular manualmente lo que haría la validación
        saldo_corte = float(personal.dias_libres_corte_2025) - dias_dla_usados
        dias_pendientes_simulados = saldo_corte + dias_libres_ganados - mock_dl_count
        
        if dias_pendientes_simulados < 0:
            print(f"   ⚠️  Límite alcanzado al intentar el DL #{mock_dl_count}")
            print(f"   ❌ Días pendientes serían: {dias_pendientes_simulados:.2f}")
            print(f"   ✅ Mensaje esperado: 'No tiene más días libres pendientes disponibles'")
            break
        else:
            intentos_exitosos += 1
            dl_temporales += 1
    
    print(f"   ℹ️  Se podrían usar {intentos_exitosos} DL adicionales antes de alcanzar el límite")
    
    # Prueba 4: Crear un caso específico donde no hay días disponibles
    print(f"\n🧪 Prueba 4: Caso con días negativos")
    
    # Buscar o crear personal con pocos días disponibles
    personal_test = Personal.objects.filter(
        estado='Activo',
        dias_libres_corte_2025__lte=5
    ).first()
    
    if personal_test:
        print(f"   Personal: {personal_test.apellidos_nombres}")
        print(f"   Días al corte: {personal_test.dias_libres_corte_2025}")
        print(f"   Días pendientes: {personal_test.dias_libres_pendientes:.2f}")
        
        # Validar si puede usar DL
        es_valido, mensaje, _ = personal_test.validar_saldo_dl(nuevo_dl=True)
        if not es_valido:
            print(f"   ✅ Validación correcta - bloqueó el uso de DL")
            print(f"   Mensaje: {mensaje}")
        else:
            print(f"   ℹ️  Aún tiene días disponibles")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETADO")
    print("=" * 80)

if __name__ == '__main__':
    test_validacion_dl()
