"""
Comando para crear superusuario automáticamente si no existe.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea un superusuario inicial si no existe'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@csrt.com',
                password='AdminCSRT2026!'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superusuario "admin" creado exitosamente'))
            self.stdout.write(self.style.WARNING('  Username: admin'))
            self.stdout.write(self.style.WARNING('  Password: AdminCSRT2026!'))
            self.stdout.write(self.style.WARNING('  ⚠️  CAMBIAR CONTRASEÑA DESPUÉS DEL PRIMER LOGIN'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Superusuario ya existe'))
