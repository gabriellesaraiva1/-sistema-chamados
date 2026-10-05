from enum import Enum

from pydantic import BaseModel


class Prioridade(str, Enum):
    baixa = "BAIXA"
    media = "MEDIA"
    alta = "ALTA"


class Status(str, Enum):
    aberto = "ABERTO"
    em_andamento = "EM_ANDAMENTO"
    resolvido = "RESOLVIDO"


class Chamado(BaseModel):
    titulo: str
    descricao: str
    prioridade: Prioridade
    usuario_id: int


class AtualizarStatus(BaseModel):
    status: Status


class ChamadoResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    prioridade: Prioridade
    status: Status
    usuario_id: int

    class Config:
        from_attributes = True