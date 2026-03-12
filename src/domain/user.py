from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class User:
    id: int
    nome: str
    dt_nascimento: date
    status: bool
    telefones: tuple[str, ...]
