from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import ChamadoDB, UsuarioDB
from schemas.chamado import (
    Chamado,
    ChamadoResponse,
    AtualizarStatus
)


router = APIRouter(
    prefix="/chamados",
    tags=["Chamados"]
)


# ==========================================
# CREATE - Criar chamado
# ==========================================

@router.post("/", response_model=ChamadoResponse)
def criar_chamado(
    chamado: Chamado,
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == chamado.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    novo_chamado = ChamadoDB(
        titulo=chamado.titulo,
        descricao=chamado.descricao,
        prioridade=chamado.prioridade.value,
        usuario_id=chamado.usuario_id
    )

    db.add(novo_chamado)
    db.commit()
    db.refresh(novo_chamado)

    return novo_chamado


# ==========================================
# READ - Listar chamados
# Filtros + Paginação + Ordenação
# ==========================================

@router.get("/", response_model=list[ChamadoResponse])
def listar_chamados(
    status: str | None = None,
    prioridade: str | None = None,
    usuario_id: int | None = None,

    # Paginação
    skip: int = Query(
        0,
        ge=0
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db)
):
    consulta = db.query(ChamadoDB)

    # ==========================================
    # FILTRO POR STATUS
    # ==========================================

    if status:
        consulta = consulta.filter(
            ChamadoDB.status == status.upper()
        )

    # ==========================================
    # FILTRO POR PRIORIDADE
    # ==========================================

    if prioridade:
        consulta = consulta.filter(
            ChamadoDB.prioridade == prioridade.upper()
        )

    # ==========================================
    # FILTRO POR USUÁRIO
    # ==========================================

    if usuario_id:
        consulta = consulta.filter(
            ChamadoDB.usuario_id == usuario_id
        )

    # ==========================================
    # ORDENAR DO MAIS RECENTE PARA O MAIS ANTIGO
    # ==========================================

    consulta = consulta.order_by(
        ChamadoDB.id.desc()
    )

    # ==========================================
    # PAGINAÇÃO
    # ==========================================

    chamados = consulta.offset(skip).limit(limit).all()

    return chamados


# ==========================================
# READ - Buscar chamado por ID
# ==========================================

@router.get("/{chamado_id}", response_model=ChamadoResponse)
def buscar_chamado(
    chamado_id: int,
    db: Session = Depends(get_db)
):
    chamado = db.query(ChamadoDB).filter(
        ChamadoDB.id == chamado_id
    ).first()

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado"
        )

    return chamado


# ==========================================
# UPDATE - Atualizar chamado
# ==========================================

@router.put("/{chamado_id}", response_model=ChamadoResponse)
def atualizar_chamado(
    chamado_id: int,
    dados: Chamado,
    db: Session = Depends(get_db)
):
    chamado = db.query(ChamadoDB).filter(
        ChamadoDB.id == chamado_id
    ).first()

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado"
        )

    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == dados.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    chamado.titulo = dados.titulo
    chamado.descricao = dados.descricao
    chamado.prioridade = dados.prioridade.value
    chamado.usuario_id = dados.usuario_id

    db.commit()
    db.refresh(chamado)

    return chamado


# ==========================================
# DELETE - Deletar chamado
# ==========================================

@router.delete("/{chamado_id}")
def deletar_chamado(
    chamado_id: int,
    db: Session = Depends(get_db)
):
    chamado = db.query(ChamadoDB).filter(
        ChamadoDB.id == chamado_id
    ).first()

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado"
        )

    db.delete(chamado)
    db.commit()

    return {
        "mensagem": "Chamado deletado com sucesso"
    }


# ==========================================
# UPDATE - Alterar status
# ==========================================

@router.patch(
    "/{chamado_id}/status",
    response_model=ChamadoResponse
)
def atualizar_status(
    chamado_id: int,
    dados: AtualizarStatus,
    db: Session = Depends(get_db)
):
    chamado = db.query(ChamadoDB).filter(
        ChamadoDB.id == chamado_id
    ).first()

    if not chamado:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado"
        )

    status_atual = chamado.status
    novo_status = dados.status.value

    # ==========================================
    # ABERTO → EM_ANDAMENTO
    # ==========================================

    if (
        status_atual == "ABERTO"
        and novo_status != "EM_ANDAMENTO"
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Um chamado ABERTO só pode "
                "ir para EM_ANDAMENTO"
            )
        )

    # ==========================================
    # EM_ANDAMENTO → RESOLVIDO
    # ==========================================

    if (
        status_atual == "EM_ANDAMENTO"
        and novo_status != "RESOLVIDO"
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Um chamado EM_ANDAMENTO só pode "
                "ir para RESOLVIDO"
            )
        )

    # ==========================================
    # RESOLVIDO não pode voltar
    # ==========================================

    if status_atual == "RESOLVIDO":
        raise HTTPException(
            status_code=400,
            detail=(
                "Um chamado RESOLVIDO não pode "
                "ter o status alterado"
            )
        )

    chamado.status = novo_status

    db.commit()
    db.refresh(chamado)

    return chamado