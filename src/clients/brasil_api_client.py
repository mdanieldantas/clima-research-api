"""Cliente HTTP para Brasil API (fallback para dados geográficos)."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

# Endpoint base da Brasil API
BRASIL_API_BASE_URL = "https://brasilapi.com.br/api"


async def get_cities_by_state(state_code: str) -> list[dict[str, object]]:
    """Busca lista de cidades de um estado na Brasil API.
    
    Args:
        state_code: Código do estado (ex.: "SP", "RJ")
    
    Returns:
        Lista de dicionários com dados de cidades
    
    Raises:
        httpx.HTTPError: Se houver erro na requisição
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{BRASIL_API_BASE_URL}/ibge/municipios/v1/{state_code}"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Brasil API: obtidas {len(data)} cidades de {state_code}")
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"Brasil API: erro HTTP {e.response.status_code} para estado {state_code}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Brasil API: erro de requisição para estado {state_code}: {e}")
            raise


async def search_city_by_name(city_name: str, state_code: str | None = None) -> dict[str, object] | None:
    """Busca uma cidade pelo nome na Brasil API.
    
    Args:
        city_name: Nome da cidade
        state_code: Código do estado (opcional, melhora precisão)
    
    Returns:
        Dicionário com dados da cidade ou None se não encontrada
    
    Raises:
        httpx.HTTPError: Se houver erro na requisição
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{BRASIL_API_BASE_URL}/ibge/municipios/v1/{state_code}" if state_code else f"{BRASIL_API_BASE_URL}/ibge/municipios/v1"
            response = await client.get(url)
            response.raise_for_status()
            cities = response.json()
            
            for city in cities:
                if city.get("name", "").lower() == city_name.lower():
                    logger.info(f"Brasil API: encontrada cidade {city_name}")
                    return city
            
            logger.warning(f"Brasil API: cidade {city_name} não encontrada")
            return None
        except httpx.RequestError as e:
            logger.error(f"Brasil API: erro ao buscar cidade {city_name}: {e}")
            raise
