from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: int
    error_code: str
    message: str
    details: Optional[Any] = None
