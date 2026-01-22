#!/usr/bin/env python
"""
Script para diagnosticar problemas con borradores.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from personal.models import Roster, Personal

print("=" * 60)
print("DIAGNÓSTICO DE BORRADORES")
print("=" * 60)

# Listar todos los roster por estado
print("\n📊 ESTADÍSTICAS DE ROSTER POR ESTADO:")
for estado in ['borrador', 'pendiente', 'aprobado']:
    count = Roster.objects.filter(estado=estado).count()
    print(f"   {estado.upper()}: {count}")

# Mostrar últimos cambios
print("\n📋 ÚLTIMOS 10 CAMBIOS EN ROSTER:")
rosters = Roster.objects.select_related('personal', 'modificado_por').order_by('-actualizado_en')[:10]
for r in rosters:
    print(f"   - {r.fecha} | {r.personal.apellidos_nombres} | {r.codigo} | Estado: {r.estado}")
    if r.modificado_por:
        print(f"     Modificado por: {r.modificado_por.username}")

# Verificar usuarios con borradores
print("\n👥 USUARIOS CON BORRADORES:")
usuarios_con_borradores = {}
for roster in Roster.objects.filter(estado='borrador').select_related('personal', 'modificado_por'):
    username = roster.modificado_por.username if roster.modificado_por else 'Desconocido'
    if username not in usuarios_con_borradores:
        usuarios_con_borradores[username] = 0
    usuarios_con_borradores[username] += 1

if usuarios_con_borradores:
    for username, count in usuarios_con_borradores.items():
        print(f"   - {username}: {count} borrador(es)")
else:
    print("   ❌ No hay borradores en el sistema")

# Verificar personal vinculado
print("\n🔗 VERIFICACIÓN DE VINCULACIÓN:")
usuarios = User.objects.filter(is_superuser=False, is_staff=True)
for user in usuarios:
    if hasattr(user, 'personal_data') and user.personal_data:
        borradores = Roster.objects.filter(
            personal=user.personal_data,
            estado='borrador'
        ).count()
        print(f"   - {user.username} → {user.personal_data.apellidos_nombres}")
        print(f"     Borradores: {borradores}")
    else:
        print(f"   - {user.username} → ❌ NO VINCULADO")

print("\n" + "=" * 60)
print("✅ Diagnóstico completado")
print("=" * 60)
