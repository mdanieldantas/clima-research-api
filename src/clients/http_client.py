"""AsyncHTTPClient reutilizável para requisições HTTP."""

from __future__ import annotations

import httpx


DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 2
DEFAULT_BACKOFF_FACTOR = 0.5


class AsyncHTTPClient:
    """Cliente HTTP assíncrono com timeout e retry padrão."""

    def __init__(
        self,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
    ) -> None:
        """Inicializa cliente HTTP."""
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Faz requisição GET."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            return await client.get(url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Faz requisição POST."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            return await client.post(url, **kwargs)
