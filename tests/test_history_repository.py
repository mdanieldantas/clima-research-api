from datetime import datetime, timezone

from src.core.database import Base, get_engine, get_session_factory
from src.repositories.history_repository import agg_series_by_city, list_by_city, save_query


def _make_session():
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = get_session_factory(engine)
    return SessionLocal()


def test_save_query_persists_entry() -> None:
    session = _make_session()

    try:
        entry = save_query(
            session,
            {
                "city_name": "Curitiba",
                "state_code": "PR",
                "latitude": -25.4284,
                "longitude": -49.2733,
                "weather_summary": "Céu limpo",
                "temperature": 22.5,
                "temperature_min": 18.2,
                "temperature_max": 24.8,
                "source_city_api": "IBGE",
                "source_weather_api": "Open-Meteo",
            },
        )

        assert entry.id is not None
        assert entry.city_name == "Curitiba"
        assert entry.queried_at.tzinfo == timezone.utc
    finally:
        session.close()


def test_list_by_city_orders_descending_and_aggregates() -> None:
    session = _make_session()

    try:
        save_query(
            session,
            {
                "city_name": "Curitiba",
                "state_code": "PR",
                "latitude": -25.4284,
                "longitude": -49.2733,
                "weather_summary": "Nublado",
                "temperature": 20.0,
                "temperature_min": 18.0,
                "temperature_max": 22.0,
                "queried_at": datetime(2026, 5, 25, 10, 0, tzinfo=timezone.utc),
                "source_city_api": "IBGE",
                "source_weather_api": "Open-Meteo",
            },
        )
        save_query(
            session,
            {
                "city_name": "Curitiba",
                "state_code": "PR",
                "latitude": -25.4284,
                "longitude": -49.2733,
                "weather_summary": "Céu limpo",
                "temperature": 23.0,
                "temperature_min": 19.0,
                "temperature_max": 25.0,
                "queried_at": datetime(2026, 5, 25, 11, 0, tzinfo=timezone.utc),
                "source_city_api": "IBGE",
                "source_weather_api": "Open-Meteo",
            },
        )
        save_query(
            session,
            {
                "city_name": "Curitiba",
                "state_code": "PR",
                "latitude": -25.4284,
                "longitude": -49.2733,
                "weather_summary": "Chuva leve",
                "temperature": 21.0,
                "temperature_min": 17.0,
                "temperature_max": 23.0,
                "queried_at": datetime(2026, 5, 25, 12, 0, tzinfo=timezone.utc),
                "source_city_api": "IBGE",
                "source_weather_api": "Open-Meteo",
            },
        )

        rows = list_by_city(session, "  curitiba  ")
        assert [row.temperature for row in rows] == [21.0, 23.0, 20.0]

        aggregates = agg_series_by_city(session, "Curitiba")
        assert aggregates["count"] == 3
        assert aggregates["temperature_min"] == 17.0
        assert aggregates["temperature_max"] == 25.0
        assert aggregates["temperature_avg"] == 21.333333333333332
        assert aggregates["last_queried_at"] == datetime(2026, 5, 25, 12, 0, tzinfo=timezone.utc)
    finally:
        session.close()
