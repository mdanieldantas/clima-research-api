"""Testes para clientes HTTP (validação de estrutura e mocking)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.clients import brasil_api_client, ibge_client, open_meteo_client


def test_ibge_client_has_required_functions() -> None:
    """Verifica que ibge_client tem as funções esperadas."""
    assert hasattr(ibge_client, "get_cities_by_state")
    assert hasattr(ibge_client, "search_city_by_name")
    assert hasattr(ibge_client, "IBGE_BASE_URL")
    assert "ibge.gov.br" in ibge_client.IBGE_BASE_URL


def test_brasil_api_client_has_required_functions() -> None:
    """Verifica que brasil_api_client tem as funções esperadas."""
    assert hasattr(brasil_api_client, "get_cities_by_state")
    assert hasattr(brasil_api_client, "search_city_by_name")
    assert hasattr(brasil_api_client, "BRASIL_API_BASE_URL")
    assert "brasilapi.com.br" in brasil_api_client.BRASIL_API_BASE_URL


def test_open_meteo_client_has_required_functions() -> None:
    """Verifica que open_meteo_client tem as funções esperadas."""
    assert hasattr(open_meteo_client, "fetch_weather")
    assert hasattr(open_meteo_client, "OPEN_METEO_BASE_URL")
    assert "open-meteo.com" in open_meteo_client.OPEN_METEO_BASE_URL


def test_http_client_wrapper_exists() -> None:
    """Verifica que http_client.py tem wrapper adequado."""
    from src.utils import http_client
    assert hasattr(http_client, "AsyncHTTPClient")
    assert hasattr(http_client, "DEFAULT_TIMEOUT")
    assert hasattr(http_client, "DEFAULT_RETRIES")


def test_clients_module_is_importable() -> None:
    """Verifica que o módulo clients pode ser importado."""
    from src import clients
    assert clients is not None

