from pydantic import BaseModel


class Usuario(BaseModel):
    nome: str
    email: str
    setor: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    setor: str

    class Config:
        from_attributes = True