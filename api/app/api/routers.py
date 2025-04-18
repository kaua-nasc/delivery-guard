from fastapi import APIRouter

from .endpoints import (
    users,
    auth,
    transactions,
#    customers
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Usuários"]
)

# api_router.include_router(
#     customers.router,
#     prefix="/customers",
#     tags=["Clientes"]
# )

api_router.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["Transações"]
)
