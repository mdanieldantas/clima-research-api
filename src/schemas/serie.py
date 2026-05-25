from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel


class SeriePoint(BaseModel):
    date: date
    temperature: float


class SerieResponse(BaseModel):
    city_name: str
    start_date: date
    end_date: date
    count: int
    average_temperature: float
    min_temperature: float
    max_temperature: float
    series: List[SeriePoint]
