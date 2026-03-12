from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from application.commands import SaveUserCommand
from domain.user import User


class UserRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    id: int = Field(gt=0)
    nome: str = Field(min_length=1, max_length=120)
    dt_nascimento: date = Field(alias="dtNascimento")
    status: bool
    telefones: list[str] = Field(default_factory=list)

    def to_command(self) -> SaveUserCommand:
        return SaveUserCommand(
            id=self.id,
            nome=self.nome,
            dt_nascimento=self.dt_nascimento,
            status=self.status,
            telefones=tuple(self.telefones),
        )


class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    nome: str
    dt_nascimento: date = Field(alias="dtNascimento")
    status: bool
    telefones: list[str]

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            nome=user.nome,
            dtNascimento=user.dt_nascimento,
            status=user.status,
            telefones=list(user.telefones),
        )
