# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session 
from typing import Generator
from app.core.config import settings

# Engine conexao com a BD
# echo=True imprime o SQL no terminal(debug)
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

# SessionLocal cria as sessoes da BD
# cada request http vai ter sua propria sessao
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Generator e a funcao que usa o yield para gerir o ciclo de vida da sess
# abre a sessao, cede para o endpoint usar, fecha no final
# fastAPI usa como dependencia injetavel
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()