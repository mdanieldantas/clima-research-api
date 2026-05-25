"""Configuração base da aplicação."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


def _parse_cors_origins(raw_value: str | None) -> tuple[str, ...]:
    if not raw_value:
        return (
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        )

    origins = tuple(
        origin.strip()
        for origin in raw_value.split(",")
        if origin.strip()
    )
    return origins or (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    )


@dataclass(frozen=True)
class Settings:
    app_name: str = "API de Pesquisa em Clima"
    app_version: str = "1.0.0"
    database_url: str | None = None
    cors_origins: tuple[str, ...] = ()

    @property
    def database_status(self) -> str:
        return "conectado" if self.database_url else "desconectado"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "API de Pesquisa em Clima"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        database_url=os.getenv("DATABASE_URL") or None,
        cors_origins=_parse_cors_origins(os.getenv("CORS_ORIGINS")),
    )
