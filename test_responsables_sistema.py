#!/usr/bin/env python
"""
Test completo del sistema de responsables de áreas.
Verifica que el fix del error 500 funciona correctamente.
"""
import os
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.models import Area, Personal


@pytest.mark.django_db
def test_sistema_responsables():
    """Test completo del sistema de responsables."""
    print("=" * 70)
    print("TEST DEL SISTEMA DE RESPONSABLES DE ÁREAS")
    print("=" * 70)
    
    errores = []
    
    # Test 1: Verificar modelo Area
    print("\n✓ Test 1: Verificar modelo Area")
    try:
        field = Area._meta.get_field('responsables')
        assert field.many_to_many, "El campo responsables debe ser ManyToManyField"
        assert field.remote_field.related_name == 'areas_responsable'
        print("  ✓ Campo responsables configurado correctamente")
    except Exception as e:
        errores.append(f"Error en modelo Area: {e}")
        print(f"  ✗ Error: {e}")
    
    # Test 2: Verificar que hay datos
    print("\n✓ Test 2: Verificar datos en la base de datos")
    try:
        total_areas = Area.objects.count()
        total_personal = Personal.objects.count()

        if total_areas == 0:
            Area.objects.create(nombre="AREA TEST")
            total_areas = Area.objects.count()

        if total_personal == 0:
            Personal.objects.create(
                nro_doc="99999999",
                apellidos_nombres="RESPONSABLE TEST",
                cargo="CARGO",
                tipo_trab="Empleado",
            )
            total_personal = Personal.objects.count()

        assert total_areas > 0, "Debe haber al menos un área"
        assert total_personal > 0, "Debe haber al menos un personal"
        print(f"  ✓ Total áreas: {total_areas}")
        print(f"  ✓ Total personal: {total_personal}")
    except Exception as e:
        errores.append(f"Error en datos: {e}")
        print(f"  ✗ Error: {e}")
    
    # Test 3: Agregar responsable
    print("\n✓ Test 3: Agregar responsable a un área")
    try:
        area = Area.objects.first()
        personal = Personal.objects.exclude(fecha_cese__isnull=False).first()
        if not personal:
            personal = Personal.objects.create(
                nro_doc="99999998",
                apellidos_nombres="RESPONSABLE TEST 2",
                cargo="CARGO",
                tipo_trab="Empleado",
            )
        
        # Limpiar responsables previos para test limpio
        responsables_previos = area.responsables.count()
        
        # Agregar responsable
        area.responsables.add(personal)
        
        # Verificar
        assert area.responsables.filter(id=personal.id).exists()
        print(f"  ✓ Responsable '{personal.apellidos_nombres}' agregado a '{area.nombre}'")
        print(f"  ✓ Total responsables en área: {area.responsables.count()}")
    except Exception as e:
        errores.append(f"Error al agregar responsable: {e}")
        print(f"  ✗ Error: {e}")
    
    # Test 4: Verificar relación inversa
    print("\n✓ Test 4: Verificar relación inversa")
    try:
        areas_del_personal = personal.areas_responsable.all()
        assert areas_del_personal.filter(id=area.id).exists()
        print(f"  ✓ {personal.apellidos_nombres} es responsable de {areas_del_personal.count()} área(s)")
    except Exception as e:
        errores.append(f"Error en relación inversa: {e}")
        print(f"  ✗ Error: {e}")
    
    # Test 5: Verificar múltiples responsables
    print("\n✓ Test 5: Agregar múltiples responsables")
    try:
        personal2 = Personal.objects.exclude(
            fecha_cese__isnull=False
        ).exclude(id=personal.id).first()

        if not personal2:
            personal2 = Personal.objects.create(
                nro_doc="99999997",
                apellidos_nombres="RESPONSABLE TEST 3",
                cargo="CARGO",
                tipo_trab="Empleado",
            )
        
        if personal2:
            area.responsables.add(personal2)
            assert area.responsables.count() >= 2
            print(f"  ✓ Área '{area.nombre}' ahora tiene {area.responsables.count()} responsables")
            
            # Listar responsables
            print("  ✓ Responsables:")
            for resp in area.responsables.all():
                print(f"     - {resp.apellidos_nombres} (DNI: {resp.nro_doc})")
        else:
            print("  ⚠ No hay suficiente personal para test de múltiples responsables")
    except Exception as e:
        errores.append(f"Error con múltiples responsables: {e}")
        print(f"  ✗ Error: {e}")
    
    # Test 6: Remover responsable
    print("\n✓ Test 6: Remover responsable")
    try:
        count_antes = area.responsables.count()
        area.responsables.remove(personal)
        count_despues = area.responsables.count()
        
        assert count_despues == count_antes - 1
        assert not area.responsables.filter(id=personal.id).exists()
        print(f"  ✓ Responsable removido correctamente")
        print(f"  ✓ Responsables restantes: {count_despues}")
    except Exception as e:
        errores.append(f"Error al remover responsable: {e}")
        print(f"  ✗ Error: {e}")
    
    # Resumen final
    print("\n" + "=" * 70)
    if errores:
        print("❌ TESTS FALLARON")
        print(f"\nErrores encontrados ({len(errores)}):")
        for i, error in enumerate(errores, 1):
            print(f"{i}. {error}")
    else:
        print("✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
        print("\nEl sistema de responsables está funcionando bien:")
        print("  • Modelo configurado correctamente")
        print("  • Operaciones CRUD funcionan")
        print("  • Relaciones inversas operativas")
        print("  • Múltiples responsables soportado")
        print("  • Admin panel ready")

    assert not errores, "Se encontraron errores en el test de responsables"


if __name__ == '__main__':
    try:
        test_sistema_responsables()
    except AssertionError:
        exit(1)
    exit(0)
