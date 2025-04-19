from fastapi import APIRouter

from .endpoints import (
    users,
    auth,
    transactions,
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    tags=["Autenticação"]
)

api_router.include_router(
    users.router,
    tags=["Usuários"]
)

api_router.include_router(
    transactions.router,
    tags=["Transações"]
)
