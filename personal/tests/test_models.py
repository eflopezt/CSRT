"""
Tests para modelos del módulo personal.
"""
import pytest
from django.contrib.auth.models import User
from personal.models import Gerencia, Area, Personal, Roster
from datetime import date
from decimal import Decimal


@pytest.mark.django_db
class TestGerencia:
    def test_crear_gerencia(self):
        gerencia = Gerencia.objects.create(
            nombre='GERENCIA DE PRUEBA',
            descripcion='Descripción de prueba'
        )
        assert gerencia.nombre == 'GERENCIA DE PRUEBA'
        assert gerencia.activa is True
        assert str(gerencia) == 'GERENCIA DE PRUEBA'


@pytest.mark.django_db
class TestArea:
    def test_crear_area(self):
        gerencia = Gerencia.objects.create(nombre='GERENCIA TEST')
        area = Area.objects.create(
            nombre='ÁREA TEST',
            gerencia=gerencia
        )
        assert area.nombre == 'ÁREA TEST'
        assert area.gerencia == gerencia
        assert str(area) == 'GERENCIA TEST - ÁREA TEST'


@pytest.mark.django_db
class TestPersonal:
    def test_crear_personal(self):
        gerencia = Gerencia.objects.create(nombre='GERENCIA TEST')
        area = Area.objects.create(nombre='ÁREA TEST', gerencia=gerencia)
        
        personal = Personal.objects.create(
            nro_doc='12345678',
            apellidos_nombres='TEST USUARIO',
            cargo='CARGO TEST',
            tipo_trab='Empleado',
            area=area,
            estado='Activo'
        )
        
        assert personal.nro_doc == '12345678'
        assert personal.esta_activo is True
        assert personal.nombre_completo == 'TEST USUARIO'


@pytest.mark.django_db
class TestRoster:
    def test_crear_roster(self):
        gerencia = Gerencia.objects.create(nombre='GERENCIA TEST')
        area = Area.objects.create(nombre='ÁREA TEST', gerencia=gerencia)
        personal = Personal.objects.create(
            nro_doc='12345678',
            apellidos_nombres='TEST USUARIO',
            cargo='CARGO TEST',
            tipo_trab='Empleado',
            area=area
        )
        
        roster = Roster.objects.create(
            personal=personal,
            fecha=date.today(),
            codigo='D',
            dias_libres_ganados=Decimal('2.5')
        )
        
        assert roster.personal == personal
        assert roster.dias_libres_ganados == Decimal('2.5')
        assert roster.codigo == 'D'
