"""Serviço de resolução e listagem de cidades."""

from __future__ import annotations

import logging

from src.clients import brasil_api_client
from src.clients import ibge_client
from src.core.exceptions import ExternalServiceError, NotFoundError
from src.utils.normalizers import normalize_city_name, normalize_state_code
from src.utils.validators import validate_city_name, validate_state_code

logger = logging.getLogger(__name__)


async def resolve(city_name: str) -> dict[str, object]:
    """Resolve coordenadas e dados de uma cidade.
    
    Tenta IBGE primeiro, depois Brasil API como fallback.
    
    Args:
        city_name: Nome da cidade a resolver
    
    Returns:
        Dicionário com {city_name, state_code, latitude, longitude, source_city_api}
    
    Raises:
        ValueError: Se city_name for inválido
        NotFoundError: Se cidade não encontrada em nenhuma API
        ExternalServiceError: Se ambas as APIs falharem
    """
    if not validate_city_name(city_name):
        raise ValueError("Nome de cidade deve ter >= 2 caracteres")
    
    normalized_city_name = normalize_city_name(city_name)
    
    # Tentar IBGE
    try:
        logger.info(f"Buscando {normalized_city_name} em IBGE...")
        result = await ibge_client.search_city_by_name(normalized_city_name)
        if result:
            return {
                "city_name": result.get("nome", normalized_city_name),
                "state_code": _extract_state_code_from_ibge_city(result),
                "latitude": float(result.get("geometria", {}).get("centroide", {}).get("coordinates", [0, 0])[1]),
                "longitude": float(result.get("geometria", {}).get("centroide", {}).get("coordinates", [0, 0])[0]),
                "source_city_api": "ibge",
            }
    except Exception as e:
        logger.warning(f"IBGE falhou para {normalized_city_name}: {e}")
    
    # Fallback: Brasil API
    try:
        logger.info(f"Buscando {normalized_city_name} em Brasil API...")
        result = await brasil_api_client.search_city_by_name(normalized_city_name)
        if result:
            return {
                "city_name": result.get("name", normalized_city_name),
                "state_code": result.get("state", "").upper(),
                "latitude": 0.0,
                "longitude": 0.0,
                "source_city_api": "brasil-api",
            }
    except Exception as e:
        logger.error(f"Brasil API falhou para {normalized_city_name}: {e}")
        raise ExternalServiceError("Serviços de cidade indisponíveis", f"IBGE e Brasil API falharam: {e}")
    
    raise NotFoundError(f"Cidade '{city_name}' não encontrada", "CITY_NOT_FOUND")


async def list_by_state(state_code: str) -> list[dict[str, object]]:
    """Lista todas as cidades de um estado.
    
    Tenta IBGE primeiro, depois Brasil API como fallback.
    
    Args:
        state_code: Código de estado (ex.: "SP", "RJ")
    
    Returns:
        Lista de dicionários com {city_name, state_code}
    
    Raises:
        ValueError: Se state_code for inválido
        NotFoundError: Se estado não encontrado
        ExternalServiceError: Se ambas as APIs falharem
    """
    if not validate_state_code(state_code):
        raise ValueError("Código de estado deve ter exatamente 2 letras")
    
    normalized_state_code = normalize_state_code(state_code)
    
    # Tentar IBGE
    try:
        logger.info(f"Listando cidades de {normalized_state_code} em IBGE...")
        cities = await ibge_client.get_cities_by_state(normalized_state_code)
        if cities:
            return [
                {
                    "city_name": city.get("nome", ""),
                    "state_code": normalized_state_code,
                }
                for city in cities
            ]
    except Exception as e:
        logger.warning(f"IBGE falhou para estado {normalized_state_code}: {e}")
    
    # Fallback: Brasil API
    try:
        logger.info(f"Listando cidades de {normalized_state_code} em Brasil API...")
        cities = await brasil_api_client.get_cities_by_state(normalized_state_code)
        if cities:
            return [
                {
                    "city_name": city.get("name", ""),
                    "state_code": normalized_state_code,
                }
                for city in cities
            ]
    except Exception as e:
        logger.error(f"Brasil API falhou para estado {normalized_state_code}: {e}")
        raise ExternalServiceError("Serviço de cidades indisponível", f"Ambas as APIs falharam: {e}")
    
    raise NotFoundError(f"Estado '{state_code}' não encontrado", "STATE_NOT_FOUND")


def _extract_state_code_from_ibge_city(city_data: dict[str, object]) -> str:
    """Extrai o código de estado de um objeto de cidade do IBGE."""
    if "microrregiao" in city_data:
        microrregiao = city_data["microrregiao"]
        if isinstance(microrregiao, dict) and "mesorregiao" in microrregiao:
            mesorregiao = microrregiao["mesorregiao"]
            if isinstance(mesorregiao, dict) and "UF" in mesorregiao:
                uf = mesorregiao["UF"]
                if isinstance(uf, dict):
                    return uf.get("sigla", "").upper()
    return ""
