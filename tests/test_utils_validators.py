"""Testes para validators."""

import pytest

from src.utils.validators import validate_city_name, validate_state_code


class TestValidateCityName:
    """Testes para validate_city_name."""

    def test_valid_city_names(self) -> None:
        """Testa nomes de cidade válidos."""
        assert validate_city_name("São Paulo")
        assert validate_city_name("Rio de Janeiro")
        assert validate_city_name("AB")
        assert validate_city_name("  Curitiba  ")

    def test_invalid_city_names(self) -> None:
        """Testa nomes de cidade inválidos."""
        assert not validate_city_name("")
        assert not validate_city_name("A")
        assert not validate_city_name("   ")
        assert not validate_city_name(None)
        assert not validate_city_name(123)


class TestValidateStateCode:
    """Testes para validate_state_code."""

    def test_valid_state_codes(self) -> None:
        """Testa códigos de estado válidos."""
        assert validate_state_code("SP")
        assert validate_state_code("sp")
        assert validate_state_code("RJ")
        assert validate_state_code("  BA  ")

    def test_invalid_state_codes(self) -> None:
        """Testa códigos de estado inválidos."""
        assert not validate_state_code("")
        assert not validate_state_code("S")
        assert not validate_state_code("SPP")
        assert not validate_state_code("1A")
        assert not validate_state_code("S1")
        assert not validate_state_code(None)
        assert not validate_state_code(12)
