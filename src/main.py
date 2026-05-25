"""Entrada principal da aplicação FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.health import router as health_router
from src.core.config import get_settings
from src.core.database import create_tables

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)


@app.on_event("startup")
def _on_startup() -> None:
    # Cria tabelas em ambiente de desenvolvimento/integração.
    create_tables()
