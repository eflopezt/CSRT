"""
Comando para limpiar la vinculación de usuarios del sistema (admin, etc).
El usuario 'admin' es superusuario y no debe tener Personal asociado.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal.models import Personal


class Command(BaseCommand):
    help = 'Limpia usuarios del sistema que no deben tener Personal asociado'

    def handle(self, *args, **options):
        # Usuarios del sistema que no deben tener Personal
        usuarios_sistema = ['admin', 'superuser']
        
        for username in usuarios_sistema:
            try:
                user = User.objects.filter(username=username).first()
                if user:
                    # Buscar si tiene Personal asociado
                    personal = Personal.objects.filter(usuario=user).first()
                    if personal:
                        self.stdout.write(
                            f'Encontrado: {username} vinculado a Personal (DNI: {personal.nro_doc})'
                        )
                        
                        # Desvincular el Personal del usuario
                        personal.usuario = None
                        personal.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Desvinculado: {username} - Personal con DNI {personal.nro_doc} ahora libre'
                            )
                        )
                    else:
                        self.stdout.write(
                            f'~ {username} - No tiene Personal asociado'
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'~ {username} - No existe')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Error con {username}: {str(e)}')
                )
