"""
Comando para crear superusuario automáticamente si no existe.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Crea un superusuario inicial si no existe'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@csrt.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'AdminCSRT2026!')
        
        if User.objects.filter(username=username).exists():
            # Si existe, actualizar la contraseña
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Contraseña del usuario "{username}" actualizada'))
        else:
            # Si no existe, crear nuevo
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Superusuario "{username}" creado exitosamente'))
        
        self.stdout.write(self.style.WARNING(f'  Username: {username}'))
        self.stdout.write(self.style.WARNING(f'  Password: {password}'))
        self.stdout.write(self.style.WARNING('  ⚠️  CAMBIAR CONTRASEÑA DESPUÉS DEL PRIMER LOGIN'))
