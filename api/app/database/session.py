from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv("DB_URL")


def get_valid_env(env: str | None):
    if env is None:
        raise 

    return env


# Crie o engine assíncrono
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

async def get_db():
    """Dependency para obter sessão do banco de dados"""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
