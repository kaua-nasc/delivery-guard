from fastapi import APIRouter, Depends, HTTPException

from ...dependencies import get_transaction_service
from ...service.transaction_service import TransactionService
from ...schemas import transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=transaction.TransactionResponse)
async def create_transaction(
        transaction_data: transaction.TransactionCreate,
        transaction_service: TransactionService = Depends(get_transaction_service)
):
    try:
        return await transaction_service.process_transaction(transaction_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))