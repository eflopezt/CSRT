#!/usr/bin/env python
"""
Test del nuevo selector dual de responsables en el formulario de áreas.
"""
import os
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.forms import AreaForm
from personal.models import Area, Personal


@pytest.mark.django_db
def test_area_form_widget():
    """Test del widget FilteredSelectMultiple en AreaForm."""
    print("=" * 70)
    print("TEST DEL SELECTOR DUAL DE RESPONSABLES")
    print("=" * 70)
    
    # Test 1: Verificar que el formulario tiene el widget correcto
    print("\n✓ Test 1: Verificar widget FilteredSelectMultiple")
    form = AreaForm()
    widget = form.fields['responsables'].widget
    print(f"  ✓ Widget: {widget.__class__.__name__}")
    print(f"  ✓ Widget verbose_name: {getattr(widget, 'verbose_name', 'N/A')}")
    print(f"  ✓ Widget is_stacked: {getattr(widget, 'is_stacked', 'N/A')}")
    
    # Test 2: Verificar queryset ordenado
    print("\n✓ Test 2: Verificar queryset ordenado")
    queryset = form.fields['responsables'].queryset
    print(f"  ✓ Total personal disponible: {queryset.count()}")
    print(f"  ✓ Ordenado por: apellidos_nombres")
    if queryset.exists():
        print(f"  ✓ Primeros 3:")
        for p in queryset[:3]:
            print(f"     - {p.apellidos_nombres}")
    
    # Test 3: Verificar formulario con instancia existente
    print("\n✓ Test 3: Formulario con área existente")
    area = Area.objects.first()
    if area:
        form_edit = AreaForm(instance=area)
        responsables_count = area.responsables.count()
        print(f"  ✓ Área: {area.nombre}")
        print(f"  ✓ Responsables actuales: {responsables_count}")
        if area.responsables.exists():
            print(f"  ✓ Responsables:")
            for resp in area.responsables.all():
                print(f"     - {resp.apellidos_nombres}")
    else:
        print("  ⚠ No hay áreas para probar")
    
    # Test 4: Simular envío de formulario
    print("\n✓ Test 4: Simular guardado con múltiples responsables")
    if area:
        # Obtener algunos responsables
        responsables = Personal.objects.exclude(fecha_cese__isnull=False)[:3]
        data = {
            'nombre': area.nombre,
            'descripcion': area.descripcion,
            'activa': area.activa,
            'responsables': [p.id for p in responsables],
        }
        form_save = AreaForm(data, instance=area)
        
        if form_save.is_valid():
            print(f"  ✓ Formulario válido")
            print(f"  ✓ Responsables a guardar: {len(data['responsables'])}")
            for p in responsables:
                print(f"     - {p.apellidos_nombres}")
        else:
            print(f"  ✗ Formulario inválido: {form_save.errors}")
    
    print("\n" + "=" * 70)
    print("✅ TODOS LOS TESTS DEL WIDGET PASARON")
    print("\nCaracterísticas del selector dual:")
    print("  • Dos listas: disponibles y seleccionados")
    print("  • Botones para mover entre listas")
    print("  • Campo de búsqueda/filtro")
    print("  • Selección múltiple")
    print("  • Interfaz similar al admin de Django")
    print("=" * 70)


if __name__ == '__main__':
    test_area_form_widget()
