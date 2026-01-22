#!/usr/bin/env python
"""
Script para verificar la vinculación entre usuarios y personal.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.models import User
from personal.models import Personal

print("=" * 60)
print("VERIFICACIÓN DE VINCULACIÓN USUARIO-PERSONAL")
print("=" * 60)

# Listar todos los usuarios
usuarios = User.objects.all().order_by('username')
print(f"\n📋 Total de usuarios: {usuarios.count()}")

for user in usuarios:
    print(f"\n👤 Usuario: {user.username}")
    print(f"   - ID: {user.id}")
    print(f"   - Email: {user.email or 'N/A'}")
    print(f"   - Es admin: {user.is_superuser}")
    print(f"   - Es staff: {user.is_staff}")
    
    # Verificar si tiene personal_data
    if hasattr(user, 'personal_data'):
        try:
            personal = user.personal_data
            if personal:
                print(f"   ✅ VINCULADO a Personal:")
                print(f"      - ID Personal: {personal.id}")
                print(f"      - DNI: {personal.nro_doc}")
                print(f"      - Nombre: {personal.nombre_completo}")
                print(f"      - Estado: {personal.estado}")
                print(f"      - Área: {personal.area.nombre if personal.area else 'Sin área'}")
            else:
                print(f"   ❌ NO VINCULADO (personal_data es None)")
        except Personal.DoesNotExist:
            print(f"   ❌ NO VINCULADO (Personal.DoesNotExist)")
    else:
        print(f"   ❌ NO VINCULADO (no tiene atributo personal_data)")

# Listar personal sin usuario
print("\n" + "=" * 60)
personal_sin_usuario = Personal.objects.filter(usuario__isnull=True, estado='Activo')
print(f"📋 Personal activo sin usuario: {personal_sin_usuario.count()}")

for p in personal_sin_usuario[:10]:  # Mostrar solo los primeros 10
    print(f"   - {p.nro_doc} - {p.nombre_completo}")

print("\n" + "=" * 60)
print("✅ Verificación completada")
print("=" * 60)
