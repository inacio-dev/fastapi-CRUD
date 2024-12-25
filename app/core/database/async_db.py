import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

# Construir URL do banco de dados usando variáveis de ambiente
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")

SQLALCHEMY_ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Configuração do engine assíncrono
async_engine = create_async_engine(
    SQLALCHEMY_ASYNC_DATABASE_URL,
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
    pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "1800")),
)

AsyncSessionLocal = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


# Função para obter sessões assíncronas
async def get_async_db():
    async with AsyncSessionLocal() as session:
        # Envolver o comando em text()
        await session.execute(text(f"SET search_path TO {POSTGRES_SCHEMA}"))
        yield session
