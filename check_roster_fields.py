#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('/workspaces/gestion-personal-nuevo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from personal.models import Roster

print("Campos del modelo Roster:")
for field in Roster._meta.get_fields():
    print(f"  - {field.name}: {type(field).__name__}")

# Intentar obtener un roster de la BD
try:
    roster = Roster.objects.first()
    if roster:
        print("\nPrimer registro de Roster:")
        print(f"  ID: {roster.id}")
        print(f"  Personal: {roster.personal}")
        print(f"  Fecha: {roster.fecha}")
        print(f"  Codigo: {roster.codigo}")
        print(f"  Observaciones: {roster.observaciones}")
        
        # Verificar si tiene el atributo dias_libres_ganados
        if hasattr(roster, 'dias_libres_ganados'):
            print(f"  ⚠️ TIENE dias_libres_ganados: {roster.dias_libres_ganados}")
        else:
            print(f"  ✓ NO tiene dias_libres_ganados (correcto)")
except Exception as e:
    print(f"Error: {e}")
