"""
Tests for validators in personal.validators.
"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from personal.models import Area, Personal, Roster, SubArea
from personal.validators import AreaValidator, PersonalValidator, RosterValidator


@pytest.mark.django_db
class TestPersonalValidator:
    def test_validar_nro_doc_dni_valido(self):
        assert PersonalValidator.validar_nro_doc("12345678") == "12345678"

    def test_validar_nro_doc_dni_invalido(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_nro_doc("1234")

    def test_validar_nro_doc_ce_valido(self):
        assert PersonalValidator.validar_nro_doc("123456789", tipo_doc="CE") == "123456789"

    def test_validar_nro_doc_ce_invalido(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_nro_doc("12345678", tipo_doc="CE")

    def test_validar_nro_doc_pasaporte_valido(self):
        assert PersonalValidator.validar_nro_doc("ABCD12345", tipo_doc="Pasaporte") == "ABCD12345"

    def test_validar_nro_doc_pasaporte_invalido(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_nro_doc("AB12", tipo_doc="Pasaporte")

    def test_validar_regimen_turno_valido(self):
        assert PersonalValidator.validar_regimen_turno("21x7") == (21, 7)

    def test_validar_regimen_turno_invalido_formato(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_regimen_turno("abc")

    def test_validar_regimen_turno_invalido_rango(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_regimen_turno("0x7")

    def test_validar_rango_fechas_valido(self):
        inicio, fin = PersonalValidator.validar_rango_fechas("2025-01-01", "2025-01-31")
        assert inicio == date(2025, 1, 1)
        assert fin == date(2025, 1, 31)

    def test_validar_rango_fechas_fin_antes(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_rango_fechas("2025-02-01", "2025-01-31")

    def test_validar_rango_fechas_formato_invalido(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_rango_fechas("2025/01/01")

    def test_validar_monto_valido(self):
        assert PersonalValidator.validar_monto("10.50", campo="sueldo") == Decimal("10.50")

    def test_validar_monto_invalido(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_monto("abc", campo="sueldo")

    def test_validar_monto_min_max(self):
        with pytest.raises(ValidationError):
            PersonalValidator.validar_monto("5", campo="sueldo", minimo=10)
        with pytest.raises(ValidationError):
            PersonalValidator.validar_monto("101", campo="sueldo", minimo=0, maximo=100)


@pytest.mark.django_db
class TestRosterValidator:
    def test_validar_codigo_valido(self):
        assert RosterValidator.validar_codigo("t") == "T"

    def test_validar_codigo_invalido(self):
        with pytest.raises(ValidationError):
            RosterValidator.validar_codigo("X")

    def test_validar_fecha_edicion_superuser(self):
        user = User.objects.create(username="admin", is_superuser=True)
        assert RosterValidator.validar_fecha_edicion("2020-01-01", user) is True

    def test_validar_fecha_edicion_pasada(self):
        user = User.objects.create(username="usuario", is_superuser=False)
        fecha = date.today() - timedelta(days=1)
        with pytest.raises(ValidationError):
            RosterValidator.validar_fecha_edicion(fecha, user)

    def test_validar_duplicado(self):
        area = Area.objects.create(nombre="AREA TEST")
        subarea = SubArea.objects.create(nombre="SUBAREA TEST", area=area)
        personal = Personal.objects.create(
            nro_doc="12345678",
            apellidos_nombres="TEST PERSONA",
            cargo="CARGO",
            tipo_trab="Empleado",
            subarea=subarea,
        )
        fecha = date.today()
        roster = Roster.objects.create(personal=personal, fecha=fecha, codigo="D")

        with pytest.raises(ValidationError):
            RosterValidator.validar_duplicado(personal, fecha)

        assert RosterValidator.validar_duplicado(personal, fecha, roster_id=roster.id) is True


@pytest.mark.django_db
class TestAreaValidator:
    def test_responsable_multiple_areas_permitido(self):
        responsable = Personal.objects.create(
            nro_doc="87654321",
            apellidos_nombres="RESPONSABLE TEST",
            cargo="CARGO",
            tipo_trab="Empleado",
        )
        area_uno = Area.objects.create(nombre="AREA UNO")
        area_uno.responsables.add(responsable)
        area_dos = Area.objects.create(nombre="AREA DOS")
        area_dos.responsables.add(responsable)

        assert AreaValidator.validar_responsable_unico(responsable) is True
