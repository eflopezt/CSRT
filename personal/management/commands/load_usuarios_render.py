"""
Comando para cargar usuarios con sus DNI en Render.
Los usuarios creados sin Personal asociado en el admin.
Vincula los DNI como contraseña.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal.models import Personal


# Lista de usuarios: (username, dni)
USUARIOS_RENDER = [
    ('jacuña', '48000903'),
    ('galfaro', '75682513'),
    ('fapaza', '46059797'),
    ('earroyo', '77420354'),
    ('latahuaman', '45917823'),
    ('ratoche', '43935996'),
    ('vaurich', '46127028'),
    ('nbedoya', '75337871'),
    ('mcabrera', '77296315'),
    ('jcaniza', '005892606'),
    ('fcasanova', '72217746'),
    ('jcastañeda', '70024630'),
    ('acastillo', '005835751'),
    ('gcastillo', '73111816'),
    ('ccastro', '10105707'),
    ('jcenturion', '73202371'),
    ('jcruz', '70689003'),
    ('acruzado', '47110375'),
    ('hcruzado', '43801267'),
    ('vcuellar', '007453650'),
    ('lcuya', '08851995'),
    ('ediaz', '72268347'),
    ('gdomenack', '47544426'),
    ('wdurand', '47281542'),
    ('jendara', '46686215'),
    ('cespejo', '41598491'),
    ('yespejo', '74144528'),
    ('gestrada', '76801259'),
    ('jferrer', '43495610'),
    ('jflores', '47964954'),
    ('gfuentes', '76306720'),
    ('fgonzales', '70495252'),
    ('jguerrero', '43382768'),
    ('egutierrez', '005419022'),
    ('ehuaytan', '45796382'),
    ('mla', '70614124'),
    ('mliza', '73147728'),
    ('elopez', '70919188'),
    ('glozada', '46137298'),
    ('jlujan', '74076597'),
    ('jluna', '43156036'),
    ('amendez', '10515850'),
    ('jmendoza', '21811280'),
    ('kmeza', '41496841'),
    ('gmorales', '73644767'),
    ('joliva', '47987309'),
    ('folivera', '73194963'),
    ('goyarce', '78286420'),
    ('cpaico', '72459185'),
    ('lpalaco', '44233779'),
    ('rpalma', '32136077'),
    ('mparrilla', '47583164'),
    ('jpastor', '44666461'),
    ('cperez', '74716792'),
    ('apiña', '73014549'),
    ('mponce', '72573615'),
    ('ppuma', '77059328'),
    ('equispe', '21261940'),
    ('mquispe', '41248182'),
    ('wquispe', '43738113'),
    ('framierz', '45096017'),
    ('wramirez', '45674438'),
    ('tramirez', '70784205'),
    ('jreyes', '70202786'),
    ('mrodriguez', '70830057'),
    ('frodriguez', '76807186'),
    ('jrojas', '76587790'),
    ('crojas', '70003871'),
    ('yruiz', '10714475'),
    ('gsalas', '46750155'),
    ('asamudio', '42791076'),
    ('wsánchez', '72440813'),
    ('dsiguenza', '74078233'),
    ('jsilva', '73481466'),
    ('isilva', '71574176'),
    ('ssolano', '45857954'),
    ('bsotacuro', '62140146'),
    ('mtalledo', '72942596'),
    ('ctirado', '43454812'),
    ('cucañay', '72686304'),
    ('nvasquez', '46734880'),
    ('cvicente', '47832664'),
    ('fvilchez', '41296195'),
    ('jvilla', '47069792'),
    ('jvillanueva', '70462078'),
    ('evillanueva', '72901854'),
    ('jzavala', '45231234'),
    ('fzavaleta', '42066622'),
    ('azelada', '70337517'),
    ('fzunini', '70079643'),
]


class Command(BaseCommand):
    help = 'Carga usuarios con DNI como contraseña para Render'

    def handle(self, *args, **options):
        creados = 0
        actualizados = 0
        errores = 0
        conflictos_dni = []

        for username, dni in USUARIOS_RENDER:
            try:
                # Verificar si el DNI ya existe en otro usuario
                dni_existente = Personal.objects.filter(nro_doc=dni).first()
                if dni_existente and dni_existente.usuario and dni_existente.usuario.username != username:
                    conflictos_dni.append({
                        'username': username,
                        'dni': dni,
                        'existente_en': dni_existente.usuario.username,
                        'accion': 'Ignorado - DNI ya vinculado'
                    })
                    continue

                # Obtener o crear el usuario Django
                user, user_created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'password': dni,  # Se setea aquí pero se hashea después
                    }
                )

                # Hashear la contraseña
                user.set_password(dni)
                user.save()

                # Obtener o crear el registro de Personal
                personal, personal_created = Personal.objects.get_or_create(
                    nro_doc=dni,
                    defaults={
                        'usuario': user,
                        'apellidos_nombres': username.upper(),
                        'tipo_doc': 'DNI',
                        'cargo': 'Pendiente',
                        'tipo_trab': 'Empleado',
                    }
                )

                # Si el Personal ya existía, vincularlo con el usuario
                if not personal_created:
                    if personal.usuario is None:
                        personal.usuario = user
                        personal.save()
                        actualizados += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'✓ Actualizado: {username} (DNI: {dni}) - Vinculado a Personal existente'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'~ {username} (DNI: {dni}) - Ya vinculado con {personal.usuario.username}'
                            )
                        )
                else:
                    if user_created:
                        creados += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Creado: {username} (DNI: {dni})'
                            )
                        )
                    else:
                        actualizados += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'✓ Actualizado: {username} (DNI: {dni}) - Usuario existente'
                            )
                        )

            except Exception as e:
                errores += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'✗ Error con {username} (DNI: {dni}): {str(e)}'
                    )
                )

        # Resumen
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'Creados: {creados}'))
        self.stdout.write(self.style.WARNING(f'Actualizados: {actualizados}'))
        self.stdout.write(self.style.ERROR(f'Errores: {errores}'))

        if conflictos_dni:
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.WARNING('CONFLICTOS DE DNI DETECTADOS:'))
            for conf in conflictos_dni:
                self.stdout.write(
                    f"  • {conf['username']} (DNI: {conf['dni']}) - "
                    f"Ya existe vinculado a {conf['existente_en']}"
                )
