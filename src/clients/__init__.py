"""Módulo de clientes HTTP para APIs externas."""

from . import brasil_api_client, ibge_client, open_meteo_client

__all__ = ["brasil_api_client", "ibge_client", "open_meteo_client"]
