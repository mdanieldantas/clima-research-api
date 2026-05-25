from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ClimaResponse(BaseModel):
    city: Optional[str] = None
    temperature: float
    temperature_min: float
    temperature_max: float
    weather_summary: str
    source_weather_api: Optional[str] = None
