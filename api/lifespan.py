from contextlib import asynccontextmanager
from fastapi import FastAPI

from .app.messaging.init import close_rabbitmq, connect_rabbitmq
from .app.database.base import Base
from .app.database.session import engine
from .app.models import customer, transaction, user, transaction_item 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    await connect_rabbitmq(app)
    
    yield
    
    print("Closing database connections...")
    await engine.dispose()
    await close_rabbitmq(app)