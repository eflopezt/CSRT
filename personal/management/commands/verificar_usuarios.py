"""
Comando para verificar y reparar vinculaciones usuario-personal.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal.models import Personal


class Command(BaseCommand):
    help = 'Verifica y muestra las vinculaciones entre usuarios y personal'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuario',
            type=str,
            help='Username del usuario a verificar',
        )
        parser.add_argument(
            '--vincular-dni',
            type=str,
            help='Vincular usuario con personal por DNI',
        )

    def handle(self, *args, **options):
        if options['vincular_dni'] and options['usuario']:
            # Vincular usuario con personal por DNI
            username = options['usuario']
            dni = options['vincular_dni']
            
            try:
                usuario = User.objects.get(username=username)
                personal = Personal.objects.get(nro_doc=dni)
                
                # Desvincular cualquier otro usuario que tenga este personal
                if personal.usuario and personal.usuario != usuario:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Personal ya estaba vinculado con {personal.usuario.username}. Desvinculando...'
                        )
                    )
                
                personal.usuario = usuario
                personal.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Usuario {username} vinculado con {personal.nombre_completo} (DNI: {dni})'
                    )
                )
                
                # Verificar que la vinculación funciona
                usuario.refresh_from_db()
                if hasattr(usuario, 'personal_data'):
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Vinculación verificada: usuario.personal_data existe'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ ERROR: La vinculación no funciona. usuario.personal_data no existe.'
                        )
                    )
                
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Usuario {username} no encontrado')
                )
            except Personal.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Personal con DNI {dni} no encontrado')
                )
            
            return
        
        # Mostrar todas las vinculaciones
        self.stdout.write(self.style.SUCCESS('\n=== VINCULACIONES USUARIO-PERSONAL ===\n'))
        
        if options['usuario']:
            # Verificar un usuario específico
            username = options['usuario']
            try:
                usuario = User.objects.get(username=username)
                self.mostrar_usuario(usuario)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Usuario {username} no encontrado')
                )
        else:
            # Mostrar todos los usuarios
            usuarios = User.objects.all().order_by('username')
            for usuario in usuarios:
                self.mostrar_usuario(usuario)
        
        # Mostrar personal sin usuario
        self.stdout.write(self.style.WARNING('\n=== PERSONAL SIN USUARIO ===\n'))
        personal_sin_usuario = Personal.objects.filter(
            usuario__isnull=True,
            estado='Activo'
        ).order_by('apellidos_nombres')
        
        if personal_sin_usuario.exists():
            for p in personal_sin_usuario:
                self.stdout.write(f'   📋 {p.nro_doc} - {p.nombre_completo}')
        else:
            self.stdout.write(self.style.SUCCESS('   ✅ Todo el personal activo tiene usuario'))

    def mostrar_usuario(self, usuario):
        self.stdout.write(f'\n👤 {usuario.username}')
        self.stdout.write(f'   ID: {usuario.id}')
        self.stdout.write(f'   Admin: {usuario.is_superuser}')
        
        if hasattr(usuario, 'personal_data'):
            try:
                personal = usuario.personal_data
                if personal:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'   ✅ VINCULADO: {personal.nro_doc} - {personal.nombre_completo}'
                        )
                    )
                    self.stdout.write(f'      Estado: {personal.estado}')
                    self.stdout.write(f'      Área: {personal.area.nombre if personal.area else "Sin área"}')
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  personal_data es None'))
            except Personal.DoesNotExist:
                self.stdout.write(self.style.ERROR('   ❌ Personal.DoesNotExist'))
        else:
            self.stdout.write(self.style.WARNING('   ❌ NO VINCULADO'))
