"""Cliente HTTP para API de Localidades do IBGE."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

# Endpoint base da API IBGE Localidades
IBGE_BASE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"


async def get_cities_by_state(state_code: str) -> list[dict[str, object]]:
    """Busca lista de cidades de um estado no IBGE.
    
    Args:
        state_code: Código do estado (ex.: "SP", "RJ")
    
    Returns:
        Lista de dicionários com dados de cidades (nome, código, etc.)
    
    Raises:
        httpx.HTTPError: Se houver erro na requisição
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{IBGE_BASE_URL}/{state_code}/municipios"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            logger.info(f"IBGE: obtidas {len(data)} cidades de {state_code}")
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"IBGE: erro HTTP {e.response.status_code} para estado {state_code}")
            raise
        except httpx.RequestError as e:
            logger.error(f"IBGE: erro de requisição para estado {state_code}: {e}")
            raise


async def search_city_by_name(city_name: str) -> dict[str, object] | None:
    """Busca uma cidade pelo nome (aproximado) no IBGE.
    
    Args:
        city_name: Nome da cidade
    
    Returns:
        Dicionário com dados da cidade ou None se não encontrada
    
    Raises:
        httpx.HTTPError: Se houver erro na requisição
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            url = f"{IBGE_BASE_URL}"
            response = await client.get(url)
            response.raise_for_status()
            states = response.json()
            
            for state in states:
                state_code = state.get("sigla")
                cities_url = f"{IBGE_BASE_URL}/{state_code}/municipios"
                cities_response = await client.get(cities_url)
                cities_response.raise_for_status()
                cities = cities_response.json()
                
                for city in cities:
                    if city.get("nome", "").lower() == city_name.lower():
                        logger.info(f"IBGE: encontrada cidade {city_name}")
                        return city
            
            logger.warning(f"IBGE: cidade {city_name} não encontrada")
            return None
        except httpx.RequestError as e:
            logger.error(f"IBGE: erro ao buscar cidade {city_name}: {e}")
            raise
