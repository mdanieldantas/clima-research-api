from sqlalchemy import text

from src.core.database import get_engine, get_session_factory


def test_get_engine_and_session_can_execute_simple_query() -> None:
    # Usa engine em memória para testes rápidos
    engine = get_engine("sqlite:///:memory:")
    SessionLocal = get_session_factory(engine)

    session = SessionLocal()
    try:
        result = session.execute(text("SELECT 1"))
        assert result is not None
        # fetchone may return Row object; verificar que é executável
        row = result.fetchone()
        assert row is not None
    finally:
        session.close()
