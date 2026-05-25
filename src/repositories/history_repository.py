"""Operações de persistência para o histórico de consultas de clima."""

from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from src.models.query_history import QueryHistory


def _normalize_city_name(city_name: str) -> str:
    return city_name.strip().casefold()


def save_query(session: Session, payload: Mapping[str, object]) -> QueryHistory:
    """Persiste um novo registro de histórico e devolve a instância salva."""

    entry = QueryHistory(**payload)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def list_by_city(session: Session, city_name: str, order: str = "desc") -> list[QueryHistory]:
    """Lista o histórico de uma cidade em ordem temporal configurável."""

    normalized_city_name = city_name.strip()
    if not normalized_city_name:
        return []

    order_clause = asc(QueryHistory.queried_at) if order.lower() == "asc" else desc(QueryHistory.queried_at)

    return (
        session.query(QueryHistory)
        .filter(func.lower(QueryHistory.city_name) == _normalize_city_name(normalized_city_name))
        .order_by(order_clause)
        .all()
    )


def agg_series_by_city(session: Session, city_name: str) -> dict[str, object]:
    """Retorna uma agregação simples dos registros de uma cidade."""

    normalized_city_name = city_name.strip()
    if not normalized_city_name:
        return {
            "city_name": "",
            "count": 0,
            "temperature_min": None,
            "temperature_max": None,
            "temperature_avg": None,
            "last_queried_at": None,
        }

    aggregates = (
        session.query(
            func.count(QueryHistory.id),
            func.min(QueryHistory.temperature_min),
            func.max(QueryHistory.temperature_max),
            func.avg(QueryHistory.temperature),
            func.max(QueryHistory.queried_at),
        )
        .filter(func.lower(QueryHistory.city_name) == _normalize_city_name(normalized_city_name))
        .one()
    )

    count, temperature_min, temperature_max, temperature_avg, last_queried_at = aggregates

    return {
        "city_name": normalized_city_name,
        "count": int(count or 0),
        "temperature_min": float(temperature_min) if temperature_min is not None else None,
        "temperature_max": float(temperature_max) if temperature_max is not None else None,
        "temperature_avg": float(temperature_avg) if temperature_avg is not None else None,
        "last_queried_at": last_queried_at,
    }
