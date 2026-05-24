"""Schema de resposta do endpoint de health."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    versao: str
    timestamp: str
    banco_dados: str
