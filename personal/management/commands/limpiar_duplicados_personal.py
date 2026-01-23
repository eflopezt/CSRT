"""
Comando para limpiar duplicados de Personal vinculados al mismo usuario.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal.models import Personal
from django.db.models import Count


class Command(BaseCommand):
    help = 'Elimina registros duplicados de Personal vinculados al mismo usuario'

    def handle(self, *args, **options):
        # Buscar usuarios con múltiples Personal vinculados
        duplicados = User.objects.annotate(
            personal_count=Count('personal_data')
        ).filter(personal_count__gt=1)

        if not duplicados.exists():
            self.stdout.write(self.style.SUCCESS('✓ No hay duplicados encontrados'))
            return

        total_eliminados = 0

        for user in duplicados:
            personales = Personal.objects.filter(usuario=user)
            self.stdout.write(
                f'\nUsuario: {user.username} tiene {personales.count()} registros Personal:'
            )

            # Mantener el primero, eliminar el resto
            primero = personales.first()
            resto = personales[1:]

            self.stdout.write(
                self.style.WARNING(
                    f'  Mantener: {primero.nro_doc} - {primero.apellidos_nombres}'
                )
            )

            for personal in resto:
                self.stdout.write(
                    f'  Eliminar: {personal.nro_doc} - {personal.apellidos_nombres}'
                )
                personal.delete()
                total_eliminados += 1

        self.stdout.write('\n' + '='*60)
        self.stdout.write(
            self.style.SUCCESS(f'✓ Total eliminados: {total_eliminados}')
        )
        self.stdout.write('='*60)
