"""
Comando para crear usuarios para los responsables de area.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from personal.models import Area, Personal


class Command(BaseCommand):
    help = 'Crea usuarios para los responsables de area y configura permisos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n🔧 Creando usuarios para responsables de area...\n'))
        
        # Crear o obtener grupo "Responsable de Área"
        grupo_responsable, created = Group.objects.get_or_create(name='Responsable de Área')
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓ Grupo creado: {grupo_responsable.name}'))
            
            # Asignar permisos al grupo
            content_types = {
                'personal': ContentType.objects.get_for_model(Personal),
                'area': ContentType.objects.get_for_model(Area),
            }
            
            permisos_responsable = [
                # Permisos de Personal
                Permission.objects.get(codename='view_personal', content_type=content_types['personal']),
                Permission.objects.get(codename='change_personal', content_type=content_types['personal']),
                # Permisos de Area (solo ver)
                Permission.objects.get(codename='view_area', content_type=content_types['area']),
            ]
            
            grupo_responsable.permissions.set(permisos_responsable)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Permisos asignados al grupo'))
        else:
            self.stdout.write(self.style.WARNING(f'  ⚠ Grupo ya existe: {grupo_responsable.name}'))
        
        # Obtener areas con responsables
        areas = Area.objects.filter(responsable__isnull=False).select_related('responsable')
        
        if not areas.exists():
            self.stdout.write(self.style.WARNING('\n  ⚠ No hay areas con responsables asignados'))
            return
        
        self.stdout.write(self.style.WARNING(f'\n📋 Procesando {areas.count()} area(s)...\n'))
        
        usuarios_creados = []
        for area in areas:
            responsable = area.responsable
            
            # Crear username a partir del nombre
            # Ejemplo: "GARCÍA LÓPEZ, JUAN CARLOS" -> "jgarcia"
            nombres_completos = responsable.apellidos_nombres.strip()
            if ',' in nombres_completos:
                apellidos, nombres = nombres_completos.split(',', 1)
                primer_nombre = nombres.strip().split()[0] if nombres.strip() else ''
                primer_apellido = apellidos.strip().split()[0] if apellidos.strip() else ''
            else:
                partes = nombres_completos.split()
                primer_nombre = partes[0] if len(partes) > 0 else ''
                primer_apellido = partes[-1] if len(partes) > 1 else ''
            
            # Username: primera letra del nombre + primer apellido (minúsculas, sin acentos)
            username_base = f"{primer_nombre[0]}{primer_apellido}".lower() if primer_nombre and primer_apellido else responsable.nro_doc
            username_base = self._quitar_acentos(username_base)
            
            # Verificar si el username ya existe y agregar número si es necesario
            username = username_base
            contador = 1
            while User.objects.filter(username=username).exists():
                username = f"{username_base}{contador}"
                contador += 1
            
            # Crear usuario si no tiene uno asignado
            if not responsable.usuario:
                # Contraseña temporal: responsable123
                password = 'responsable123'
                
                user = User.objects.create_user(
                    username=username,
                    email=responsable.correo_corporativo or responsable.correo_personal or f'{username}@empresa.com',
                    password=password,
                    first_name=primer_nombre[:30],
                    last_name=primer_apellido[:150]
                )
                
                # Asignar al grupo
                user.groups.add(grupo_responsable)
                user.is_staff = True  # Puede acceder al admin si es necesario
                user.save()
                
                # Vincular usuario con personal
                responsable.usuario = user
                responsable.save()
                
                usuarios_creados.append({
                    'area': area.nombre,
                    'responsable': responsable.apellidos_nombres,
                    'username': username,
                    'password': password
                })
                
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Usuario creado: {username} para {responsable.apellidos_nombres} ({area.nombre})'
                ))
            else:
                # Ya tiene usuario, solo asegurarse de que esté en el grupo
                if not responsable.usuario.groups.filter(name='Responsable de Área').exists():
                    responsable.usuario.groups.add(grupo_responsable)
                    self.stdout.write(self.style.SUCCESS(
                        f'  ✓ Grupo asignado a: {responsable.usuario.username} ({responsable.apellidos_nombres})'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'  ⚠ Usuario ya existe: {responsable.usuario.username} ({responsable.apellidos_nombres})'
                    ))
        
        # Mostrar resumen
        if usuarios_creados:
            self.stdout.write(self.style.SUCCESS('\n✅ Usuarios creados exitosamente!\n'))
            self.stdout.write(self.style.WARNING('📝 Credenciales de acceso:\n'))
            for user_info in usuarios_creados:
                self.stdout.write(f"   {user_info['area']}:")
                self.stdout.write(f"   - Responsable: {user_info['responsable']}")
                self.stdout.write(f"   - Usuario: {user_info['username']}")
                self.stdout.write(f"   - Contraseña: {user_info['password']}\n")
        else:
            self.stdout.write(self.style.WARNING('\n⚠ No se crearon nuevos usuarios'))
    
    def _quitar_acentos(self, texto):
        """Quita acentos y caracteres especiales."""
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N', 'ü': 'u', 'Ü': 'U'
        }
        for old, new in replacements.items():
            texto = texto.replace(old, new)
        return texto
