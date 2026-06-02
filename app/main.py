from fastapi import FastAPI

from app.database import Base, engine
from app.routes import auth, users

# Cria as tabelas no banco de dados caso ainda não existam.
# Para esta prova técnica, isso simplifica a execução do projeto.
# Em produção, o ideal seria usar migrations com Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Prova Técnica - Desenvolvedor Backend",
    description=(
        "API RESTful desenvolvida em Python com FastAPI, SQLite, "
        "CRUD de usuários, autenticação JWT e integração com modelo de IA."
    ),
    version="1.0.0",
)

# Registro das rotas da aplicação.
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    """
    Rota inicial para verificar se a API está online.
    """
    return {
        "message": "API da prova técnica está online.",
        "docs": "/docs",
    }