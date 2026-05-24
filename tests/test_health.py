from datetime import datetime, timezone, timedelta

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_get_health_returns_expected_payload() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "saudavel"
    assert payload["versao"] == "1.0.0"
    assert payload["banco_dados"] in {"conectado", "desconectado"}

    timestamp = datetime.fromisoformat(payload["timestamp"])
    assert timestamp.tzinfo is not None
    assert datetime.now(timezone.utc) - timestamp < timedelta(seconds=5)
