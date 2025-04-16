from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.controllers.fraud_controller import router

app = FastAPI(
    title="Delivery",
    description="API para analisar e listar possíveis fraudes em compras online.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/fraude", tags=["Fraudes"])
