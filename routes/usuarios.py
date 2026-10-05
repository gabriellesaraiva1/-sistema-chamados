from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioDB
from schemas.usuario import Usuario, UsuarioResponse


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# CREATE
@router.post("/", response_model=UsuarioResponse)
def criar_usuario(
    usuario: Usuario,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(UsuarioDB).filter(
        UsuarioDB.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    novo_usuario = UsuarioDB(
        nome=usuario.nome,
        email=usuario.email,
        setor=usuario.setor
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


# READ - listar todos
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioDB).all()

    return usuarios


# READ - buscar por ID
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario


# UPDATE
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: Usuario,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    usuario.nome = dados.nome
    usuario.email = dados.email
    usuario.setor = dados.setor

    db.commit()
    db.refresh(usuario)

    return usuario


# DELETE
@router.delete("/{usuario_id}")
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "mensagem": "Usuário deletado com sucesso"
    }