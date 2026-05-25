"""Testes para normalizers."""

from src.utils.normalizers import normalize_city_name, normalize_state_code, normalize_string


class TestNormalizeString:
    """Testes para normalize_string."""

    def test_trim(self) -> None:
        """Testa trim de espaços."""
        assert normalize_string("  hello  ") == "hello"

    def test_multiple_spaces(self) -> None:
        """Testa remoção de múltiplos espaços."""
        assert normalize_string("hello    world") == "hello world"

    def test_combined(self) -> None:
        """Testa combinação."""
        result = normalize_string("  São    Paulo  ")
        assert "Paulo" in result
        assert "  " not in result

    def test_non_string_input(self) -> None:
        """Testa entrada não-string."""
        assert normalize_string(None) == ""


class TestNormalizeCityName:
    """Testes para normalize_city_name."""

    def test_basic_normalization(self) -> None:
        """Testa normalização básica."""
        assert normalize_city_name("Rio  de   Janeiro") == "Rio de Janeiro"

    def test_trim(self) -> None:
        """Testa trim."""
        assert normalize_city_name("  São Paulo  ") == normalize_city_name("São Paulo")


class TestNormalizeStateCode:
    """Testes para normalize_state_code."""

    def test_lowercase_to_uppercase(self) -> None:
        """Testa conversão para maiúsculas."""
        assert normalize_state_code("sp") == "SP"
        assert normalize_state_code("ba") == "BA"

    def test_trim_and_uppercase(self) -> None:
        """Testa trim e maiúsculas."""
        assert normalize_state_code("  sp  ") == "SP"
        assert normalize_state_code("  rj  ") == "RJ"
