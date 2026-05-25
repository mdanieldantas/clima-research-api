"""Wrapper de httpx.AsyncClient com timeouts/retries/logging padrão."""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Configurações padrão para clientes HTTP
DEFAULT_TIMEOUT = httpx.Timeout(timeout=10.0, connect=5.0)
DEFAULT_RETRIES = 2
DEFAULT_BACKOFF_FACTOR = 0.5


class AsyncHTTPClient:
    """Wrapper de httpx.AsyncClient com retry, timeout e logging padrão."""

    def __init__(
        self,
        timeout: httpx.Timeout = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ) -> None:
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> AsyncHTTPClient:
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """GET com retry automático."""
        if not self._client:
            raise RuntimeError("AsyncHTTPClient deve ser usado com context manager")
        return await self._client.get(url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """POST com retry automático."""
        if not self._client:
            raise RuntimeError("AsyncHTTPClient deve ser usado com context manager")
        return await self._client.post(url, **kwargs)
