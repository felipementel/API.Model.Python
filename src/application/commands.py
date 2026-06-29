"""Command objects for the application use-case layer."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class SaveUserCommand:
    """Immutable command carrying the data needed to save a user."""

    id: int
    nome: str
    dt_nascimento: date
    status: bool
    telefones: tuple[str, ...]
