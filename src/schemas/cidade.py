from __future__ import annotations

from pydantic import BaseModel


class CidadeResponse(BaseModel):
    city_name: str
    state_code: str
    latitude: float
    longitude: float
    source_city_api: str
