"""
Comando para sincronizar usuarios con personal.
Automatiza la vinculación de usuarios existentes y creación de nuevos usuarios.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
from personal.models import Personal
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sincroniza usuarios con personal: vincula existentes y crea faltantes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--crear-usuarios',
            action='store_true',
            help='Crear usuarios para personal que no tiene usuario asignado'
        )
        parser.add_argument(
            '--vincular-existentes',
            action='store_true',
            help='Vincular usuarios existentes con personal por DNI'
        )
        parser.add_argument(
            '--password-default',
            type=str,
            default='dni',
            help='Contraseña por defecto: "dni" usa el DNI, o especificar otra (default: dni)'
        )
        parser.add_argument(
            '--solo-activos',
            action='store_true',
            help='Procesar solo personal con estado Activo'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular sin hacer cambios reales'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        crear_usuarios = options['crear_usuarios']
        vincular_existentes = options['vincular_existentes']
        password_default = options['password_default']
        solo_activos = options['solo_activos']

        # Si no se especifica ninguna opción, hacer ambas
        if not crear_usuarios and not vincular_existentes:
            crear_usuarios = True
            vincular_existentes = True

        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODO SIMULACIÓN (dry-run) - No se realizarán cambios'))

        # Filtrar personal
        personal_qs = Personal.objects.select_related('usuario', 'subarea__area')
        if solo_activos:
            personal_qs = personal_qs.filter(estado='Activo')

        self.stdout.write(f'\n📊 Total de personal a procesar: {personal_qs.count()}')

        # Estadísticas
        stats = {
            'vinculados': 0,
            'creados': 0,
            'ya_vinculados': 0,
            'errores': 0,
            'personal_sin_dni': 0
        }

        # 1. VINCULAR USUARIOS EXISTENTES
        if vincular_existentes:
            self.stdout.write(self.style.MIGRATE_HEADING('\n🔗 VINCULANDO USUARIOS EXISTENTES...'))
            stats_vinc = self._vincular_usuarios_existentes(personal_qs, dry_run)
            stats['vinculados'] = stats_vinc['vinculados']
            stats['ya_vinculados'] = stats_vinc['ya_vinculados']
            stats['errores'] += stats_vinc['errores']

        # 2. CREAR USUARIOS NUEVOS
        if crear_usuarios:
            self.stdout.write(self.style.MIGRATE_HEADING('\n👤 CREANDO USUARIOS FALTANTES...'))
            stats_crear = self._crear_usuarios_faltantes(personal_qs, password_default, dry_run)
            stats['creados'] = stats_crear['creados']
            stats['personal_sin_dni'] = stats_crear['sin_dni']
            stats['errores'] += stats_crear['errores']

        # RESUMEN FINAL
        self._mostrar_resumen(stats, dry_run)

    def _vincular_usuarios_existentes(self, personal_qs, dry_run):
        """Vincula usuarios existentes con personal por DNI."""
        stats = {'vinculados': 0, 'ya_vinculados': 0, 'errores': 0}

        # Obtener personal sin usuario asignado
        personal_sin_usuario = personal_qs.filter(usuario__isnull=True)

        for persona in personal_sin_usuario:
            if not persona.nro_doc or persona.tipo_doc != 'DNI':
                continue

            try:
                # Generar username esperado: primera letra nombre + apellido paterno
                nombres = persona.apellidos_nombres.strip().split()
                if len(nombres) < 2:
                    continue
                
                apellido_paterno = nombres[0].lower()
                primer_nombre = nombres[-1] if len(nombres) >= 2 else nombres[0]
                primera_letra = primer_nombre[0].lower()
                username_esperado = f'{primera_letra}{apellido_paterno}'.lower()
                
                # Buscar usuario con ese username o variaciones (username1, username2, etc.)
                usuario = None
                try:
                    usuario = User.objects.get(username=username_esperado)
                except User.DoesNotExist:
                    # Buscar variaciones con número
                    for i in range(1, 10):
                        try:
                            usuario = User.objects.get(username=f'{username_esperado}{i}')
                            break
                        except User.DoesNotExist:
                            continue
                
                if not usuario:
                    continue

                # Verificar que el usuario no esté vinculado a otro personal
                if hasattr(usuario, 'personal_data'):
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠️  Usuario {usuario.username} ya está vinculado a {usuario.personal_data}'
                        )
                    )
                    continue

                if not dry_run:
                    persona.usuario = usuario
                    persona.save(update_fields=['usuario'])

                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Vinculado: {persona.apellidos_nombres} ({persona.nro_doc}) → Usuario {usuario.username}'
                    )
                )
                stats['vinculados'] += 1

            except User.DoesNotExist:
                # No existe usuario con ese DNI, se creará después si se especificó
                pass
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error vinculando {persona.nro_doc}: {str(e)}')
                )
                stats['errores'] += 1

        # Contar personal ya vinculado
        stats['ya_vinculados'] = personal_qs.filter(usuario__isnull=False).count()

        return stats

    def _crear_usuarios_faltantes(self, personal_qs, password_default, dry_run):
        """Crea usuarios para personal que no tiene usuario asignado."""
        stats = {'creados': 0, 'sin_dni': 0, 'errores': 0}

        # Obtener personal sin usuario que tenga DNI
        personal_sin_usuario = personal_qs.filter(
            usuario__isnull=True,
            tipo_doc='DNI'
        ).exclude(nro_doc__isnull=True).exclude(nro_doc='')

        if personal_sin_usuario.count() == 0:
            self.stdout.write(self.style.SUCCESS('  ℹ️  No hay personal sin usuario para crear'))
            return stats

        for persona in personal_sin_usuario:
            try:
                # Generar username: primera letra nombre + apellido paterno
                nombres = persona.apellidos_nombres.strip().split()
                if len(nombres) < 2:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠️  {persona.apellidos_nombres} no tiene formato válido para generar username'
                        )
                    )
                    continue
                
                # Apellido paterno + Apellido materno + Nombres
                # Asumir que primeros 2 son apellidos, resto nombres
                apellido_paterno = nombres[0].lower()
                primer_nombre = nombres[-1] if len(nombres) >= 2 else nombres[0]
                primera_letra = primer_nombre[0].lower()
                username = f'{primera_letra}{apellido_paterno}'.lower()
                
                # Si ya existe, agregar número
                username_base = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f'{username_base}{counter}'
                    counter += 1
                    if counter > 99:
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ No se pudo generar username único para {persona.apellidos_nombres}')
                        )
                        stats['errores'] += 1
                        break
                
                if counter > 99:
                    continue

                # Generar email
                email = persona.correo_corporativo or persona.correo_personal or f'{username}@temp.com'

                # Extraer nombres para first_name y last_name
                first_name = ' '.join(nombres[2:]) if len(nombres) > 2 else nombres[-1]  # Nombres
                last_name = ' '.join(nombres[:2]) if len(nombres) >= 2 else nombres[0]  # Apellidos
                
                # Contraseña: DNI o personalizada
                password = persona.nro_doc if password_default.lower() == 'dni' else password_default

                if not dry_run:
                    with transaction.atomic():
                        # Crear usuario
                        usuario = User.objects.create_user(
                            username=username,
                            email=email,
                            password=password,
                            first_name=first_name[:30],
                            last_name=last_name[:30],
                            is_staff=False,
                            is_active=True
                        )

                        # Vincular con personal
                        persona.usuario = usuario
                        persona.save(update_fields=['usuario'])

                        # Agregar a grupo según rol (opcional)
                        # Si es responsable de área, agregar al grupo correspondiente
                        if hasattr(persona, 'area_responsable'):
                            grupo, _ = Group.objects.get_or_create(name='Responsable de Área')
                            usuario.groups.add(grupo)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Creado: {persona.apellidos_nombres} → Usuario: {username} | Password: {password}'
                    )
                )
                stats['creados'] += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ✗ Error creando usuario para {persona.apellidos_nombres} ({persona.nro_doc}): {str(e)}'
                    )
                )
                stats['errores'] += 1
                logger.error(f"Error creando usuario para {persona.nro_doc}: {str(e)}", exc_info=True)

        # Contar personal sin DNI
        stats['sin_dni'] = personal_qs.filter(usuario__isnull=True).exclude(tipo_doc='DNI').count()

        return stats

    def _mostrar_resumen(self, stats, dry_run):
        """Muestra un resumen de las operaciones realizadas."""
        self.stdout.write(self.style.MIGRATE_HEADING('\n' + '='*60))
        self.stdout.write(self.style.MIGRATE_HEADING('📋 RESUMEN DE SINCRONIZACIÓN'))
        self.stdout.write(self.style.MIGRATE_HEADING('='*60))

        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  Modo simulación - No se realizaron cambios reales'))

        self.stdout.write(f'\n✅ Personal ya vinculado: {stats["ya_vinculados"]}')
        self.stdout.write(self.style.SUCCESS(f'🔗 Usuarios vinculados: {stats["vinculados"]}'))
        self.stdout.write(self.style.SUCCESS(f'👤 Usuarios creados: {stats["creados"]}'))

        if stats['personal_sin_dni'] > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Personal sin DNI (no se puede crear usuario): {stats["personal_sin_dni"]}'
                )
            )

        if stats['errores'] > 0:
            self.stdout.write(self.style.ERROR(f'❌ Errores: {stats["errores"]}'))

        self.stdout.write(f'\n{"="*60}\n')

        if not dry_run and stats['creados'] > 0:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  IMPORTANTE: Los nuevos usuarios deben cambiar su contraseña en el primer inicio de sesión.'
                )
            )
