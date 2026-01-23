"""
Comando para limpiar usuarios con nombres incorrectos (con prefijos).
Libera los DNI para que puedan ser vinculados a los usuarios correctos.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal.models import Personal


# Mapeo de usuarios incorrectos -> correcto
USUARIOS_INCORRECTOS = {
    'tacuña': 'jacuña',
    'xalfaro': 'galfaro',
    'oatahuaman': 'latahuaman',
    'aatoche': 'ratoche',
    'aaurich': 'vaurich',
    'abedoya': 'nbedoya',
    'dcabrera': 'mcabrera',
    'ecasanova': 'fcasanova',
    'acastañeda': 'jcastañeda',
    'ecastillo': 'gcastillo',
    'rcastro': 'ccastro',
    'acenturion': 'jcenturion',
    'acruz': 'jcruz',
    'fcruzado': 'hcruzado',
    'ecuya1': 'lcuya',
    'cdomenack': 'gdomenack',
    'hdurand': 'wdurand',
    'aendara': 'jendara',
    'oespejo': 'cespejo',
    'aespejo': 'yespejo',
    'pestrada': 'gestrada',
    'cflores': 'jflores',
    'jfuentes': 'gfuentes',
    'jgonzales': 'fgonzales',
    'jguerrero1': 'jguerrero',
    'gla': 'mla',
    'pliza': 'mliza',
    'glujan': 'jlujan',
    'cluna': 'jluna',
    'cmendoza': 'jmendoza',
    'fmorales': 'gmorales',
    'toliva': 'joliva',
    'aolivera': 'folivera',
    'loyarce': 'goyarce',
    'apaico': 'cpaico',
    'jpalaco': 'lpalaco',
    'rpalma1': 'rpalma',
    'bpastor': 'jpastor',
    'aperez': 'cperez',
    'aponce': 'mponce',
    'tpuma': 'ppuma',
    'jquispe': 'equispe',
    'aquispe': 'mquispe',
    'kquispe': 'wquispe',
    'rramierz': 'framierz',
    'eramirez': 'wramirez',
    'aramirez': 'tramirez',
    'preyes': 'jreyes',
    'arodriguez': 'mrodriguez',
    'arodriguez1': 'frodriguez',
    'arojas': 'jrojas',
    'frojas': 'crojas',
    'oruiz': 'yruiz',
    'asalas': 'gsalas',
    'rsamudio': 'asamudio',
    'asánchez': 'wsánchez',
    'nsilva': 'isilva',
    'rsolano': 'ssolano',
    'psotacuro': 'bsotacuro',
    'etalledo': 'mtalledo',
    'rtirado': 'ctirado',
    'eucañay': 'cucañay',
    'evasquez': 'nvasquez',
    'kvicente': 'cvicente',
    'fvilchez1': 'fvilchez',
    'yvillanueva': 'evillanueva',
    'lzavala': 'jzavala',
    'jzelada': 'azelada',
    'tzunini': 'fzunini',
}


class Command(BaseCommand):
    help = 'Elimina usuarios con nombres incorrectos y libera sus DNI'

    def handle(self, *args, **options):
        eliminados = 0
        no_encontrados = 0
        errores = 0

        for username_incorrecto, username_correcto in USUARIOS_INCORRECTOS.items():
            try:
                user = User.objects.filter(username=username_incorrecto).first()
                if user:
                    personal = Personal.objects.filter(usuario=user).first()
                    if personal:
                        dni = personal.nro_doc
                        self.stdout.write(
                            f'Eliminando: {username_incorrecto} (DNI: {dni}) → '
                            f'será reemplazado por {username_correcto}'
                        )
                        user.delete()
                        eliminados += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Usuario {username_incorrecto} eliminado'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'~ {username_incorrecto} sin Personal asociado'
                            )
                        )
                else:
                    no_encontrados += 1
                    self.stdout.write(
                        self.style.WARNING(f'~ {username_incorrecto} no existe')
                    )

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error eliminando {username_incorrecto}: {str(e)}'
                    )
                )

        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Eliminados: {eliminados}'))
        self.stdout.write(self.style.WARNING(f'No encontrados: {no_encontrados}'))
        self.stdout.write(self.style.ERROR(f'Errores: {errores}'))
        self.stdout.write(
            '\nAhora ejecuta: python manage.py load_usuarios_render'
        )
        self.stdout.write('='*60)
