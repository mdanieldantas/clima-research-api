"""Configuração do engine e sessão SQLAlchemy."""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from src.core.config import get_settings

Base = declarative_base()


def get_engine(database_url: str | None = None) -> Engine:
    """Cria e retorna um Engine SQLAlchemy.

    Se `database_url` for None, usa SQLite em arquivo `./dev.db`.
    """
    settings = get_settings()
    url = database_url or settings.database_url or "sqlite:///./dev.db"
    # echo=False para evitar poluição de logs por padrão
    return create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite:") else {})


# Session factory padrão (pode ser sobrescrita em testes)
def get_session_factory(engine: Engine | None = None) -> sessionmaker:
    eng = engine or get_engine()
    return sessionmaker(bind=eng, autocommit=False, autoflush=False)


def get_db(engine: Engine | None = None) -> Generator[Session, None, None]:
    """Dependência / gerador para obter uma sessão DB.

    Uso em FastAPI: `Depends(get_db)` (quando usando `Depends` com callables síncronos,
    passe `lambda: next(get_db())` ou use uma função wrapper). Em testes, importar e
    chamar este gerador diretamente para obter sessão.
    """
    SessionLocal = get_session_factory(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables(engine: Engine | None = None) -> None:
    """Cria todas as tabelas registradas em `Base` no banco configurado."""
    eng = engine or get_engine()
    Base.metadata.create_all(bind=eng)
