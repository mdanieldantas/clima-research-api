"""Schemas Pydantic da aplicação."""

from .health import HealthResponse
from .error import ErrorResponse
from .clima import ClimaResponse
from .cidade import CidadeResponse
from .historico import HistoricoItem
from .serie import SerieResponse, SeriePoint

__all__ = [
	"HealthResponse",
	"ErrorResponse",
	"ClimaResponse",
	"CidadeResponse",
	"HistoricoItem",
	"SerieResponse",
	"SeriePoint",
]
