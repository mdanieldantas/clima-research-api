"""Normalizadores de strings para a API."""

from __future__ import annotations

import unicodedata


def normalize_string(text: str) -> str:
    """Normaliza uma string: trim, remove múltiplos espaços, unicode normalize.
    
    Args:
        text: String a normalizar
    
    Returns:
        String normalizada
    """
    if not isinstance(text, str):
        return ""
    
    # Unicode normalize (NFKD para preservar a maioria dos acentos)
    normalized = unicodedata.normalize("NFKD", text)
    
    # Trim
    normalized = normalized.strip()
    
    # Remover múltiplos espaços
    normalized = " ".join(normalized.split())
    
    return normalized


def normalize_city_name(city_name: str) -> str:
    """Normaliza o nome de uma cidade.
    
    Args:
        city_name: Nome da cidade
    
    Returns:
        Nome normalizado
    """
    return normalize_string(city_name)


def normalize_state_code(state_code: str) -> str:
    """Normaliza um código de estado (UF) para maiúscula.
    
    Args:
        state_code: Código de estado
    
    Returns:
        Código normalizado em maiúscula
    """
    return normalize_string(state_code).upper()
