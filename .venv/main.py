from fastapi import FastAPI

from database import engine, Base
from routes.usuarios import router as usuarios_router
from routes.chamados import router as chamados_router
from routes.relatorios import router as relatorios_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Chamados",
    description="API para gerenciamento de chamados de suporte",
    version="1.0.0"
)


app.include_router(usuarios_router)
app.include_router(chamados_router)
app.include_router(relatorios_router)


@app.get("/")
def inicio():
    return {
        "mensagem": "Sistema de Chamados funcionando!"
    }