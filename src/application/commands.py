from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class SaveUserCommand:
    id: int
    nome: str
    dt_nascimento: date
    status: bool
    telefones: tuple[str, ...]
