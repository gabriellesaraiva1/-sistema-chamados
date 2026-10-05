from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    setor = Column(String, nullable=False)

    chamados = relationship(
        "ChamadoDB",
        back_populates="usuario"
    )


class ChamadoDB(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, index=True)

    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)

    prioridade = Column(String, nullable=False)
    status = Column(
        String,
        nullable=False,
        default="ABERTO"
    )

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    usuario = relationship(
        "UsuarioDB",
        back_populates="chamados"
    )
