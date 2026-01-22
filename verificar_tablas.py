#!/usr/bin/env python
"""
Script para verificar el nombre de las tablas en la base de datos.
Ejecutar antes de hacer deploy a Render.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection

print("=" * 60)
print("VERIFICACIÓN DE TABLAS - PRE DEPLOY")
print("=" * 60)
print()

# Obtener nombre de la base de datos
db_name = connection.settings_dict.get('NAME', 'N/A')
print(f"📊 Base de datos actual: {db_name}")
print()

# Listar todas las tablas relacionadas con 'roster'
with connection.cursor() as cursor:
    # Para SQLite
    if 'sqlite' in connection.settings_dict['ENGINE']:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%roster%' ORDER BY name;"
        )
    # Para PostgreSQL
    else:
        cursor.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename LIKE '%roster%' ORDER BY tablename;"
        )
    
    tablas = cursor.fetchall()
    
    if tablas:
        print("📋 Tablas encontradas con 'roster' en el nombre:")
        print()
        for tabla in tablas:
            nombre_tabla = tabla[0]
            print(f"   • {nombre_tabla}")
            
            # Verificar si es el nombre correcto
            if 'rooster' in nombre_tabla.lower():
                print(f"     ⚠️  WARNING: Tabla con doble 'o' detectada!")
                print(f"     ➜  Debes renombrarla a: {nombre_tabla.replace('rooster', 'roster')}")
            elif 'roster' in nombre_tabla.lower():
                print(f"     ✅ Nombre correcto")
        print()
    else:
        print("⚠️  No se encontraron tablas con 'roster' en el nombre")
        print()

# Verificar que el modelo Roster funciona
print("-" * 60)
print("🔍 Verificando modelo Roster...")
print()

try:
    from personal.models import Roster
    
    # Intentar hacer una consulta simple
    total = Roster.objects.count()
    print(f"✅ Modelo Roster funciona correctamente")
    print(f"   Total de registros: {total}")
    
    # Verificar campos nuevos
    if hasattr(Roster, 'estado'):
        print(f"✅ Campo 'estado' existe en el modelo")
        
        # Ver distribución de estados
        from django.db.models import Count
        estados = Roster.objects.values('estado').annotate(count=Count('id'))
        if estados:
            print(f"   Distribución de estados:")
            for estado in estados:
                print(f"      • {estado['estado']}: {estado['count']} registros")
    else:
        print(f"❌ Campo 'estado' NO existe (migración no aplicada)")
    
except Exception as e:
    print(f"❌ Error al verificar modelo: {e}")

print()
print("=" * 60)
print("RESUMEN")
print("=" * 60)
print()

# Determinar si está listo para deploy
if tablas:
    tiene_rooster = any('rooster' in t[0].lower() for t in tablas)
    if tiene_rooster:
        print("⚠️  ACCIÓN REQUERIDA:")
        print("   Debes renombrar las tablas antes de hacer deploy a Render")
        print()
        print("   SQL para ejecutar en Render:")
        print("   ALTER TABLE personal_rooster RENAME TO personal_roster;")
        print("   ALTER TABLE personal_roosteraudit RENAME TO personal_rosteraudit;")
        print()
    else:
        print("✅ LISTO PARA DEPLOY")
        print("   Las tablas tienen el nombre correcto")
        print()
else:
    print("❌ NO LISTO - No se encontraron tablas")
    print()

print("=" * 60)
