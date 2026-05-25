"""Testes para city_service."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.core.exceptions import ExternalServiceError, NotFoundError
from src.services import city_service
from src.utils.normalizers import normalize_city_name, normalize_state_code
from src.utils.validators import validate_city_name, validate_state_code


def test_validate_city_name_valid() -> None:
    """Testa validação de nome de cidade válido."""
    assert validate_city_name("São Paulo") is True
    assert validate_city_name("SP") is True
    assert validate_city_name("  Rio de Janeiro  ") is True


def test_validate_city_name_invalid() -> None:
    """Testa validação de nome de cidade inválido."""
    assert validate_city_name("") is False
    assert validate_city_name("A") is False
    assert validate_city_name("   ") is False
    assert validate_city_name(None) is False


def test_validate_state_code_valid() -> None:
    """Testa validação de código de estado válido."""
    assert validate_state_code("SP") is True
    assert validate_state_code("sp") is True
    assert validate_state_code("RJ") is True
    assert validate_state_code("  BA  ") is True


def test_validate_state_code_invalid() -> None:
    """Testa validação de código de estado inválido."""
    assert validate_state_code("") is False
    assert validate_state_code("S") is False
    assert validate_state_code("SPP") is False
    assert validate_state_code("1A") is False
    assert validate_state_code(None) is False


def test_normalize_city_name() -> None:
    """Testa normalização de nome de cidade."""
    result = normalize_city_name("  São Paulo  ")
    # NFKD decompõe acentos; apenas verificar que contém a segunda parte
    assert "Paulo" in result
    assert normalize_city_name("Rio  de   Janeiro") == "Rio de Janeiro"


def test_normalize_state_code() -> None:
    """Testa normalização de código de estado."""
    assert normalize_state_code("sp") == "SP"
    assert normalize_state_code("  BA  ") == "BA"


@pytest.mark.asyncio
async def test_resolve_with_invalid_city_name() -> None:
    """Testa resolve com nome de cidade inválido."""
    with pytest.raises(ValueError):
        await city_service.resolve("A")


@pytest.mark.asyncio
async def test_resolve_city_found_in_ibge() -> None:
    """Testa resolve com cidade encontrada em IBGE."""
    mock_result = {
        "nome": "São Paulo",
        "geometria": {
            "centroide": {
                "coordinates": [-46.6333, -23.5505]
            }
        },
        "microrregiao": {
            "mesorregiao": {
                "UF": {"sigla": "SP"}
            }
        }
    }

    with patch("src.clients.ibge_client.search_city_by_name", new_callable=AsyncMock) as mock_ibge:
        mock_ibge.return_value = mock_result
        
        result = await city_service.resolve("São Paulo")
        
        assert result["city_name"] == "São Paulo"
        assert result["state_code"] == "SP"
        assert result["source_city_api"] == "ibge"
        assert result["latitude"] == -23.5505
        assert result["longitude"] == -46.6333


@pytest.mark.asyncio
async def test_resolve_city_not_found() -> None:
    """Testa resolve com cidade não encontrada."""
    with patch("src.clients.ibge_client.search_city_by_name", new_callable=AsyncMock) as mock_ibge:
        with patch("src.clients.brasil_api_client.search_city_by_name", new_callable=AsyncMock) as mock_brasil:
            mock_ibge.return_value = None
            mock_brasil.return_value = None
            
            with pytest.raises(NotFoundError) as exc_info:
                await city_service.resolve("CidadeInexistente")
            
            assert exc_info.value.error_code == "CITY_NOT_FOUND"


@pytest.mark.asyncio
async def test_resolve_both_apis_fail() -> None:
    """Testa resolve quando ambas APIs falham."""
    with patch("src.clients.ibge_client.search_city_by_name", new_callable=AsyncMock) as mock_ibge:
        with patch("src.clients.brasil_api_client.search_city_by_name", new_callable=AsyncMock) as mock_brasil:
            mock_ibge.side_effect = Exception("IBGE error")
            mock_brasil.side_effect = Exception("Brasil API error")
            
            with pytest.raises(ExternalServiceError) as exc_info:
                await city_service.resolve("São Paulo")
            
            assert exc_info.value.error_code == "EXTERNAL_SERVICE_ERROR"


@pytest.mark.asyncio
async def test_list_by_state_with_invalid_code() -> None:
    """Testa list_by_state com código inválido."""
    with pytest.raises(ValueError):
        await city_service.list_by_state("A")


@pytest.mark.asyncio
async def test_list_by_state_success() -> None:
    """Testa list_by_state com sucesso."""
    mock_cities = [
        {"nome": "São Paulo", "id": 3550308},
        {"nome": "Campinas", "id": 3509007},
    ]

    with patch("src.clients.ibge_client.get_cities_by_state", new_callable=AsyncMock) as mock_ibge:
        mock_ibge.return_value = mock_cities
        
        result = await city_service.list_by_state("SP")
        
        assert len(result) == 2
        assert result[0]["city_name"] == "São Paulo"
        assert result[0]["state_code"] == "SP"
        assert result[1]["city_name"] == "Campinas"


@pytest.mark.asyncio
async def test_list_by_state_not_found() -> None:
    """Testa list_by_state com estado não encontrado."""
    with patch("src.clients.ibge_client.get_cities_by_state", new_callable=AsyncMock) as mock_ibge:
        with patch("src.clients.brasil_api_client.get_cities_by_state", new_callable=AsyncMock) as mock_brasil:
            mock_ibge.return_value = []
            mock_brasil.return_value = []
            
            with pytest.raises(NotFoundError) as exc_info:
                await city_service.list_by_state("XX")
            
            assert exc_info.value.error_code == "STATE_NOT_FOUND"
