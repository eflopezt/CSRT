#!/usr/bin/env python
"""
Script para probar las validaciones de Roster
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.models import Area, Personal, Roster
from personal.forms import RosterForm
from django.core.exceptions import ValidationError

def test_validaciones():
    print("=" * 80)
    print("PRUEBAS DE VALIDACIONES DE ROSTER")
    print("=" * 80)
    
    # Obtener datos de prueba
    try:
        personal = Personal.objects.first()
        if not personal:
            print("❌ No hay personal en la base de datos. Ejecuta: python manage.py seed_data")
            return
        
        print(f"\n✓ Personal de prueba: {personal.nombre_completo}")
        print(f"  Días libres pendientes: {personal.dias_libres_pendientes}")
        
        # Asegurarnos de que tiene suficientes días libres para las pruebas
        dias_corte_originales = personal.dias_libres_corte_2025
        personal.dias_libres_corte_2025 = 20  # Suficientes para las pruebas
        personal.save()
        print(f"  Días libres ajustados para pruebas: {personal.dias_libres_pendientes}")
        
        # TEST 1: Validar que no se puede exceder 7 DLA consecutivos
        print("\n" + "=" * 80)
        print("TEST 1: No permitir más de 7 DLA consecutivos")
        print("=" * 80)
        
        # Crear 7 DLA consecutivos
        base_date = date.today() + timedelta(days=30)
        for i in range(7):
            fecha = base_date + timedelta(days=i)
            Roster.objects.get_or_create(
                personal=personal,
                fecha=fecha,
                defaults={'codigo': 'DLA'}
            )
        
        print(f"✓ Creados 7 DLA consecutivos desde {base_date}")
        
        # Intentar crear el 8vo DLA consecutivo
        fecha_8 = base_date + timedelta(days=7)
        try:
            roster = Roster(personal=personal, fecha=fecha_8, codigo='DLA')
            roster.full_clean()
            print("❌ ERROR: Se permitió crear el 8vo DLA consecutivo")
        except ValidationError as e:
            error_messages = str(e)
            if 'No se pueden' in error_messages and 'consecutivos' in error_messages:
                print(f"✓ VALIDACIÓN CORRECTA: No se permite el 8vo DLA consecutivo")
            else:
                print(f"❌ ERROR: Validación incorrecta: {e}")
        
        # TEST 2: Validar que los días libres disponibles no pueden ser negativos
        print("\n" + "=" * 80)
        print("TEST 2: No permitir días libres disponibles negativos")
        print("=" * 80)
        
        # Guardar días libres actuales
        dias_actuales = personal.dias_libres_corte_2025
        print(f"Días libres corte 2025: {dias_actuales}")
        
        # Intentar crear más DLA de los que tiene disponibles
        fecha_test = base_date + timedelta(days=20)
        try:
            # Forzar un escenario donde no tenga suficientes días libres
            personal.dias_libres_corte_2025 = 0
            personal.save()
            
            roster = Roster(personal=personal, fecha=fecha_test, codigo='DLA')
            roster.full_clean()
            print("❌ ERROR: Se permitió crear DLA sin días disponibles")
        except ValidationError as e:
            error_messages = str(e)
            if 'suficientes días' in error_messages or 'saldo' in error_messages.lower():
                print(f"✓ VALIDACIÓN CORRECTA: No se permite DLA sin días disponibles")
            else:
                print(f"❌ ERROR: Validación incorrecta: {e}")
        finally:
            # Restaurar días libres
            personal.dias_libres_corte_2025 = dias_actuales
            personal.save()
        
        # TEST 3: Validar formulario
        print("\n" + "=" * 80)
        print("TEST 3: Validar formulario RosterForm")
        print("=" * 80)
        
        # El 8vo DLA debe ser el día siguiente al 7mo (fecha consecutiva)
        fecha_form = base_date + timedelta(days=7)  # El día 8vo consecutivo
        form_data = {
            'personal': personal.pk,
            'fecha': fecha_form.strftime('%Y-%m-%d'),
            'codigo': 'DLA',
            'observaciones': ''
        }
        
        form = RosterForm(data=form_data)
        if form.is_valid():
            print(f"❌ ERROR: El formulario permitió más de 7 DLA consecutivos en {fecha_form}")
            print(f"   Datos del formulario: {form.cleaned_data}")
        else:
            print(f"✓ VALIDACIÓN CORRECTA DEL FORMULARIO")
        
        # TEST 4: Editar un DLA existente no debe contar doble
        print("\n" + "=" * 80)
        print("TEST 4: Editar un DLA existente no debe contar doble")
        print("=" * 80)
        
        # Obtener uno de los DLA creados
        roster_existente = Roster.objects.filter(
            personal=personal,
            fecha__gte=base_date,
            fecha__lt=base_date + timedelta(days=7),
            codigo='DLA'
        ).first()
        
        if roster_existente:
            # Intentar guardar el mismo registro sin cambios
            try:
                roster_existente.full_clean()
                print(f"✓ VALIDACIÓN CORRECTA: Se puede editar un DLA existente sin error")
            except ValidationError as e:
                print(f"❌ ERROR: No se puede editar un DLA existente: {e}")
        
        print("\n" + "=" * 80)
        print("LIMPIEZA: Eliminando datos de prueba")
        print("=" * 80)
        
        # Limpiar datos de prueba
        Roster.objects.filter(
            personal=personal,
            fecha__gte=base_date
        ).delete()
        
        # Restaurar días libres originales
        personal.dias_libres_corte_2025 = dias_corte_originales
        personal.save()
        
        print("✓ Datos de prueba eliminados y días libres restaurados")
        
        print("\n" + "=" * 80)
        print("RESUMEN DE PRUEBAS COMPLETADO")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_validaciones()
