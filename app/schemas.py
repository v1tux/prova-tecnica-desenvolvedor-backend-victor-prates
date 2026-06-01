from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Campos base compartilhados entre os schemas de usuário.
    """

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema usado para criação de usuário.

    Recebe a senha original apenas na entrada da API.
    Essa senha não deve ser retornada nas respostas.
    """

    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """
    Schema usado para atualização parcial dos dados do usuário.

    Todos os campos são opcionais para permitir atualizar apenas
    uma informação específica.
    """

    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema usado para retornar dados do usuário.

    Não inclui password nem hashed_password por segurança.
    """

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Schema de resposta do login.

    Retorna o token JWT e o tipo do token.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Dados mínimos extraídos do token JWT.
    """

    email: str | None = None