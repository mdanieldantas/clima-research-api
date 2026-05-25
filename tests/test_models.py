from datetime import timezone

from src.core.database import Base, get_engine, get_session_factory
from src.models.query_history import QueryHistory


def test_query_history_model_persists_values() -> None:
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = get_session_factory(engine)
    session = SessionLocal()

    try:
        entry = QueryHistory(
            city_name="Curitiba",
            state_code="PR",
            latitude=-25.4284,
            longitude=-49.2733,
            weather_summary="Céu limpo",
            temperature=22.5,
            temperature_min=18.2,
            temperature_max=24.8,
            source_city_api="IBGE",
            source_weather_api="Open-Meteo",
        )

        session.add(entry)
        session.commit()
        session.refresh(entry)

        persisted = session.query(QueryHistory).filter_by(id=entry.id).one()

        assert persisted.city_name == "Curitiba"
        assert persisted.state_code == "PR"
        assert persisted.latitude == -25.4284
        assert persisted.longitude == -49.2733
        assert persisted.weather_summary == "Céu limpo"
        assert persisted.temperature == 22.5
        assert persisted.temperature_min == 18.2
        assert persisted.temperature_max == 24.8
        assert persisted.source_city_api == "IBGE"
        assert persisted.source_weather_api == "Open-Meteo"
        assert persisted.queried_at.tzinfo == timezone.utc
    finally:
        session.close()