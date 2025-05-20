from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .config import DATABASE_URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_valid_env(env: str | None):
    if env is None:
        raise 

    return env

engine = create_async_engine(
    get_valid_env(DATABASE_URL),
    echo=True,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "ssl": "require"
    }
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para obter sessão do banco de dados"""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()