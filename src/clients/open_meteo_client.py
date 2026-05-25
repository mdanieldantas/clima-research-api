"""Cliente para Open-Meteo Weather API."""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger(__name__)

OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_TIMEOUT = 10


async def fetch_weather(latitude: float, longitude: float) -> dict | None:
    """Obtém dados de clima para coordenadas.
    
    Args:
        latitude: Latitude
        longitude: Longitude
        
    Returns:
        Dados de clima com temperatura, weather_code, etc
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
    }
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(OPEN_METEO_BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            current = data.get("current", {})
            return {
                "temperature": current.get("temperature_2m"),
                "weather_code": current.get("weather_code"),
                "temp_max": current.get("temperature_2m_max"),
                "temp_min": current.get("temperature_2m_min"),
            }
    except httpx.RequestError as e:
        logger.error(f"Erro ao buscar clima para ({latitude}, {longitude}): {e}")
        return None
