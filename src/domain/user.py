"""Domain entity representing a user in the system."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class User:
    """Immutable domain entity for a registered user."""

    id: int
    nome: str
    dt_nascimento: date
    status: bool
    telefones: tuple[str, ...]
