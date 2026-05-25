"""Cliente para IBGE Localidades API."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

IBGE_BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades"
DEFAULT_TIMEOUT = 10


async def get_cities_by_state(state_code: str) -> list[dict]:
    """Obtém cidades de um estado via IBGE.
    
    Args:
        state_code: Código do estado (ex: 'SP', 'RJ')
        
    Returns:
        Lista de cidades com nome, lat, lon
    """
    url = f"{IBGE_BASE_URL}/estados/{state_code}/municipios"
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [{"city_name": item["nome"], "latitude": None, "longitude": None} for item in data]
    except httpx.RequestError as e:
        logger.error(f"Erro ao buscar cidades de {state_code}: {e}")
        return []


async def search_city_by_name(city_name: str) -> dict | None:
    """Busca uma cidade pelo nome em todos os estados.
    
    Args:
        city_name: Nome da cidade
        
    Returns:
        Dados da cidade ou None
    """
    url = f"{IBGE_BASE_URL}/municipios"
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            for city in data:
                if city["nome"].lower() == city_name.lower():
                    return {"city_name": city["nome"], "latitude": None, "longitude": None}
            return None
    except httpx.RequestError as e:
        logger.error(f"Erro ao buscar cidade {city_name}: {e}")
        return None
