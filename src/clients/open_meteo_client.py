"""Cliente HTTP para Open-Meteo API (dados climáticos)."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

# Endpoint base da Open-Meteo API
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_weather(latitude: float, longitude: float) -> dict[str, object]:
    """Busca dados climáticos atuais para coordenadas.
    
    Args:
        latitude: Latitude do local
        longitude: Longitude do local
    
    Returns:
        Dicionário com dados climáticos (temperatura, vento, etc.)
    
    Raises:
        httpx.HTTPError: Se houver erro na requisição
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,weather_code,temperature_max,temperature_min",
                "timezone": "auto",
            }
            response = await client.get(OPEN_METEO_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Open-Meteo: obtidos dados climáticos para ({latitude}, {longitude})")
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"Open-Meteo: erro HTTP {e.response.status_code} para coordenadas ({latitude}, {longitude})")
            raise
        except httpx.RequestError as e:
            logger.error(f"Open-Meteo: erro de requisição para ({latitude}, {longitude}): {e}")
            raise
