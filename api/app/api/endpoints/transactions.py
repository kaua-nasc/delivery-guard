from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ...database.session import get_db
from ...models.customer import Customer
from ...models.transaction import Transaction
from ...models.transaction_item import TransactionItem
from ...schemas.transaction import TransactionCreate, TransactionResponse
from ...core.ml_service import predict_fraud

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
    "",
    summary="Listar transações recentes",
    description="Retorna uma lista das transações recentes com seus status de fraude"
)
def list_transactions():
    return {"hello": "world"}

@router.post("/transactions/", 
             response_model=TransactionResponse,
             status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    # Verifica se o cliente existe
    customer = await db.execute(
        select(Customer).filter(Customer.id == transaction_data.customer_id)
    )
    customer = customer.scalars().first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Cria a transação principal
    transaction_dict = transaction_data.dict(exclude={"items"})
    db_transaction = Transaction(**transaction_dict)
    
    # Adiciona os itens da transação
    for item in transaction_data.items:
        db_item = TransactionItem(**item.dict())
        db_transaction.items.append(db_item)

    db.add(db_transaction)
    
    try:
        # Faz commit para obter o ID da transação
        await db.commit()
        await db.refresh(db_transaction)
        
        # Chama o serviço de ML para análise (assíncrono)
        ml_result = await predict_fraud(db_transaction)
        
        # Atualiza com o resultado do ML
        db_transaction.ml_status = ml_result.status
        db_transaction.ml_score = ml_result.score
        db_transaction.ml_decision_time = datetime.now(datetime.timezone.utc)
        
        await db.commit()
        await db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )