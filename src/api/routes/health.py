"""Rota de health da aplicação."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from src.core.config import get_settings
from src.schemas.health import HealthResponse

router = APIRouter(prefix="/api/v1/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="saudavel",
        versao=settings.app_version,
        timestamp=datetime.now(timezone.utc).isoformat(),
        banco_dados=settings.database_status,
    )
