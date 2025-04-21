from ..service.customer_service import CustomerService
from ..repository.transaction_repository import TransactionRepository
from ..schemas.transaction import TransactionCreate, TransactionResponse

class TransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        customer_service: CustomerService
        #ml_service: ml_service,
        #notification_service: NotificationService
    ):
        self.transaction_repo = transaction_repo
        self.customer_service = customer_service
        

    async def process_transaction(self, transaction_data: TransactionCreate) -> TransactionResponse:
        existing = await self.transaction_repo.get_by_id(transaction_data.transaction_id)
        if existing:
            raise ValueError("Transaction ID already exists")
        
        customer = transaction_data.customer.model_dump()
        customer = await self.customer_service.get_by_id(customer["customer_id"])
        if customer is None:
            customer = await self.customer_service.create({**transaction_data.customer.model_dump()})

        transaction = transaction_data.model_dump(exclude={"customer"})
        transaction["customer_id"] = customer.id

        db_transaction = await self.transaction_repo.create({
            **transaction,
            "status": "pending"
        })
        
        return TransactionResponse.model_validate(db_transaction)