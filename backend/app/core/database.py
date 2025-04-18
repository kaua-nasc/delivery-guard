# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

# Criando a engine
engine = create_engine(settings.database_url)

# Criando o SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # Sua sessão de banco de dados
    try:
        yield db  # Retorna o objeto db para uso nas rotas
    finally:
        db.close()  # Fecha a sessão ao final
