"""Exceções customizadas da aplicação."""

from __future__ import annotations


class APIException(Exception):
    """Base para exceções da API."""

    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR", status_code: int = 500, details: str = "") -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class InvalidInputError(APIException):
    """Entrada inválida (400)."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message, "INVALID_INPUT", 400, details)


class NotFoundError(APIException):
    """Recurso não encontrado (404)."""

    def __init__(self, message: str, error_code: str = "NOT_FOUND", details: str = "") -> None:
        super().__init__(message, error_code, 404, details)


class ExternalServiceError(APIException):
    """Serviço externo indisponível (503)."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", 503, details)


class DatabaseError(APIException):
    """Erro ao acessar o banco (500)."""

    def __init__(self, message: str, details: str = "") -> None:
        super().__init__(message, "DATABASE_ERROR", 500, details)
