from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .lifespan import lifespan
from .app.api.routers import api_router

app = FastAPI(
    title="Delivery Guard API",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix="/api"
)