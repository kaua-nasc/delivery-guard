from fastapi import APIRouter, status
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operação não permitida"},
        status.HTTP_404_NOT_FOUND: {"description": "Recurso não encontrado"},
    }
)

@router.get(
    "/",
    summary="Listar transações recentes",
    description="Retorna uma lista das transações recentes com seus status de fraude"
)
def list_transactions(
):
    return {"hello": "world"}