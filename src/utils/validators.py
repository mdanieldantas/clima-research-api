"""Validadores de entrada para a API."""

from __future__ import annotations


def validate_city_name(city_name: str) -> bool:
    """Valida se um nome de cidade é válido.
    
    Args:
        city_name: Nome da cidade
    
    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(city_name, str):
        return False
    normalized = city_name.strip()
    return len(normalized) >= 2


def validate_state_code(state_code: str) -> bool:
    """Valida se um código de estado (UF) é válido.
    
    Args:
        state_code: Código de estado (2 letras)
    
    Returns:
        True se válido, False caso contrário
    """
    if not isinstance(state_code, str):
        return False
    normalized = state_code.strip().upper()
    return len(normalized) == 2 and normalized.isalpha()
