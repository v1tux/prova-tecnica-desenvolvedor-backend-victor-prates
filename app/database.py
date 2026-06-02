import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexão com o banco SQLite.
# O arquivo do banco será criado na raiz do projeto com o nome app.db.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# O parâmetro connect_args é necessário para o SQLite funcionar corretamente
# com aplicações web, permitindo o uso da conexão em diferentes threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# SessionLocal será usada para criar sessões de comunicação com o banco.
# Cada requisição da API poderá abrir uma sessão e fechá-la ao final.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base será herdada pelos models SQLAlchemy.
# É a partir dela que as tabelas serão mapeadas.
Base = declarative_base()


def get_db():
    """
    Cria uma sessão com o banco de dados para ser usada nas rotas da API.

    O uso de yield permite que o FastAPI abra a sessão durante a requisição
    e feche automaticamente ao final, mesmo se ocorrer algum erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()