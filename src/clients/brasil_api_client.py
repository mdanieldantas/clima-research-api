"""Cliente para Brasil API."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

BRASIL_API_BASE_URL = "https://brasilapi.com.br/api/ibge/municipios/v1"
DEFAULT_TIMEOUT = 10


async def get_cities_by_state(state_code: str) -> list[dict]:
    """Obtém cidades de um estado via Brasil API.
    
    Args:
        state_code: Código do estado (ex: 'SP', 'RJ')
        
    Returns:
        Lista de cidades
    """
    url = f"{BRASIL_API_BASE_URL}/{state_code}"
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return [{"city_name": city, "latitude": None, "longitude": None} for city in data]
    except httpx.RequestError as e:
        logger.error(f"Erro ao buscar cidades de {state_code}: {e}")
        return []


async def search_city_by_name(city_name: str) -> dict | None:
    """Busca uma cidade pelo nome.
    
    Args:
        city_name: Nome da cidade
        
    Returns:
        Dados da cidade ou None
    """
    # Brasil API não oferece busca por nome diretamente
    # Retorna None para usar fallback
    return None
