from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .repository.customer_repository import CustomerRepository
from .repository.transaction_repository import TransactionRepository
from .service.customer_service import CustomerService
from .service.transaction_service import TransactionService
from .database.session import get_db


def get_customer_repository(db: AsyncSession = Depends(get_db)) -> CustomerRepository:
    return CustomerRepository(db)

def get_customer_service(repo: CustomerRepository = Depends(get_customer_repository)) -> CustomerService:
    return CustomerService(repo)

def get_transaction_repository(db: AsyncSession = Depends(get_db)) -> TransactionRepository:
    return TransactionRepository(db)

def get_transaction_service(
        transaction_repo: TransactionRepository = Depends(get_transaction_repository), 
        customer_service: CustomerService = Depends(get_customer_service),
    ) -> TransactionService:
    #ml_service = MLService()
    #notification_service = NotificationService()
    return TransactionService(transaction_repo, customer_service)
