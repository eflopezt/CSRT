"""
Comando para crear datos de prueba en el sistema.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from personal.models import Area, SubArea, Personal, Roster
from datetime import date, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Crea datos de prueba en el sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-roster',
            action='store_true',
            help='Crear también registros de roster',
        )

    def handle(self, *args, **options):
        self.stdout.write('Creando datos de prueba...')

        # Crear superusuario
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superusuario admin creado (pass: admin123)'))

        # Crear areas (antes llamadas gerencias)
        areas_data = [
            {'nombre': 'GERENCIA DE OPERACIONES', 'descripcion': 'Gestión de operaciones'},
            {'nombre': 'GERENCIA DE LOGÍSTICA', 'descripcion': 'Gestión logística'},
            {'nombre': 'GERENCIA DE RECURSOS HUMANOS', 'descripcion': 'Gestión de personal'},
            {'nombre': 'GERENCIA DE FINANZAS', 'descripcion': 'Gestión financiera'},
        ]

        areas = []
        for data in areas_data:
            area, created = Area.objects.get_or_create(
                nombre=data['nombre'],
                defaults={'descripcion': data['descripcion']}
            )
            areas.append(area)
            if created:
                self.stdout.write(f'  ✓ Área creada: {area.nombre}')

        # Crear subareas
        subareas_data = [
            ('ADMINISTRACIÓN', areas[2]),
            ('LOGÍSTICA', areas[1]),
            ('MANTENIMIENTO', areas[0]),
            ('SEGURIDAD', areas[0]),
            ('FINANZAS', areas[3]),
            ('CONTABILIDAD', areas[3]),
        ]

        subareas = []
        for nombre, area in subareas_data:
            subarea, created = SubArea.objects.get_or_create(
                nombre=nombre,
                area=area,
                defaults={'descripcion': f'SubÁrea de {nombre}'}
            )
            subareas.append(subarea)
            if created:
                self.stdout.write(f'  ✓ SubÁrea creada: {subarea.nombre} ({area.nombre})')

        # Crear personal
        personal_data = [
            ('12345678', 'GARCÍA LÓPEZ, JUAN CARLOS', 'Jefe de Área', 'Empleado'),
            ('23456789', 'RODRÍGUEZ PÉREZ, MARÍA ELENA', 'Supervisora', 'Empleado'),
            ('34567890', 'FERNÁNDEZ TORRES, PEDRO LUIS', 'Operador', 'Obrero'),
            ('45678901', 'MARTÍNEZ SÁNCHEZ, ANA SOFÍA', 'Técnico', 'Obrero'),
            ('56789012', 'LÓPEZ RAMÍREZ, CARLOS ALBERTO', 'Coordinador', 'Empleado'),
            ('67890123', 'GONZÁLEZ FLORES, LAURA PATRICIA', 'Asistente', 'Empleado'),
            ('78901234', 'HERRERA CASTRO, MIGUEL ÁNGEL', 'Operador', 'Obrero'),
            ('89012345', 'SILVA MENDOZA, ROSA MARÍA', 'Analista', 'Empleado'),
        ]

        personal_list = []
        for i, (doc, nombre, cargo, tipo) in enumerate(personal_data):
            subarea = subareas[i % len(subareas)]
            personal, created = Personal.objects.get_or_create(
                nro_doc=doc,
                defaults={
                    'apellidos_nombres': nombre,
                    'cargo': cargo,
                    'tipo_trab': tipo,
                    'subarea': subarea,
                    'fecha_alta': date.today() - timedelta(days=random.randint(30, 365)),
                    'estado': 'Activo',
                    'sexo': 'M' if i % 2 == 0 else 'F',
                    'celular': f'99{random.randint(1000000, 9999999)}',
                    'correo_personal': f'usuario{i+1}@example.com',
                    'correo_corporativo': f'{nombre.split(",")[0].lower().replace(" ", ".")}@empresa.com',
                    'banco': random.choice(['BCP', 'BBVA', 'Scotiabank']),
                    'afp': random.choice(['Habitat', 'Integra', 'Prima', 'Profuturo']),
                    'sueldo_base': Decimal(random.randint(3000, 8000)),
                    'regimen_turno': random.choice(['14x7', '21x7', '28x14']),
                }
            )
            personal_list.append(personal)
            if created:
                self.stdout.write(f'  ✓ Personal creado: {nombre}')

        # Asignar responsables a areas
        for i, area in enumerate(areas):
            if not area.responsable and i < len(personal_list):
                area.responsable = personal_list[i]
                area.save()
                self.stdout.write(f'  ✓ Responsable asignado a {area.nombre}')

        # Crear roster si se especificó
        if options['with_roster']:
            self.stdout.write('Creando registros de roster...')
            # Códigos según la leyenda del roster:
            # T: Trabajo Presencial (cada 3 genera 1 día libre)
            # TR: Trabajo Remoto (cada 5 genera 2 días libres)
            # DL: Día Libre
            # DOL: Compensación por Horario Extendido
            # DM: Descanso Médico
            # V: Vacaciones Aprobadas y/o Gozadas
            # F: Feriado No Recuperable
            # FC: Feriado Compensable
            codigos = ['T', 'TR', 'DL', 'DOL', 'DM', 'V', 'F', 'FC']
            # Peso para que T y TR sean más frecuentes
            codigos_ponderados = ['T'] * 10 + ['TR'] * 8 + ['DL'] * 5 + ['DOL'] * 2 + ['DM'] * 2 + ['V'] * 3 + ['F'] * 1 + ['FC'] * 1
            fecha_inicio = date.today() - timedelta(days=30)
            
            for personal in personal_list:
                for i in range(30):
                    fecha = fecha_inicio + timedelta(days=i)
                    codigo = random.choice(codigos_ponderados)
                    
                    Roster.objects.get_or_create(
                        personal=personal,
                        fecha=fecha,
                        defaults={
                            'codigo': codigo,
                            'observaciones': 'Generado por seed_data'
                        }
                    )
                
                # Calcular días libres ganados para este personal
                count_t = Roster.objects.filter(personal=personal, codigo='T').count()
                count_tr = Roster.objects.filter(personal=personal, codigo='TR').count()
                dias_libres_t = count_t // 3
                dias_libres_tr = (count_tr // 5) * 2
                # Los dias libres ganados se calculan desde el roster, no se persisten.
            
            self.stdout.write(self.style.SUCCESS(f'✓ Roster creado para {len(personal_list)} personas'))
            self.stdout.write(self.style.SUCCESS(f'✓ Días libres calculados automáticamente'))

        self.stdout.write(self.style.SUCCESS('\n✅ Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.WARNING('\n📝 Credenciales de acceso:'))
        self.stdout.write('   Usuario: admin')
        self.stdout.write('   Contraseña: admin123')
