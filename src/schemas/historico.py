from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistoricoItem(BaseModel):
    id: Optional[int]
    city_name: str
    state_code: str
    latitude: float
    longitude: float
    weather_summary: str
    temperature: float
    temperature_min: float
    temperature_max: float
    queried_at: datetime
    source_city_api: Optional[str] = None
    source_weather_api: Optional[str] = None
