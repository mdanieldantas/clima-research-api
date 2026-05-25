"""Modelo SQLAlchemy para histórico de consultas de clima."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.types import TypeDecorator

from src.core.database import Base


def utcnow() -> datetime:
    """Retorna o instante atual em UTC com timezone explícito."""
    return datetime.now(timezone.utc)


class UTCDateTime(TypeDecorator):
    """Armazena datetimes em UTC e os devolve com timezone explícito."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime | None, dialect) -> datetime | None:
        if value is None:
            return None

        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc).replace(tzinfo=None)

    def process_result_value(self, value: datetime | None, dialect) -> datetime | None:
        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)


class QueryHistory(Base):
    """Registro persistido de uma consulta de clima."""

    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, index=True, nullable=False)
    state_code = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    weather_summary = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    temperature_min = Column(Float, nullable=False)
    temperature_max = Column(Float, nullable=False)
    queried_at = Column(UTCDateTime(), default=utcnow, nullable=False)
    source_city_api = Column(String, nullable=True)
    source_weather_api = Column(String, nullable=True)