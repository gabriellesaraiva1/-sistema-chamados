from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import ChamadoDB


router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)


@router.get("/chamados")
def relatorio_chamados(
    db: Session = Depends(get_db)
):
    total = db.query(ChamadoDB).count()

    abertos = db.query(ChamadoDB).filter(
        ChamadoDB.status == "ABERTO"
    ).count()

    em_andamento = db.query(ChamadoDB).filter(
        ChamadoDB.status == "EM_ANDAMENTO"
    ).count()

    resolvidos = db.query(ChamadoDB).filter(
        ChamadoDB.status == "RESOLVIDO"
    ).count()

    prioridade_alta = db.query(ChamadoDB).filter(
        ChamadoDB.prioridade == "ALTA"
    ).count()

    return {
        "total": total,
        "abertos": abertos,
        "em_andamento": em_andamento,
        "resolvidos": resolvidos,
        "prioridade_alta": prioridade_alta
    }