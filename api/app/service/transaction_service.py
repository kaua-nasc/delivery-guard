from ..messaging.producer import RabbitMQProducer
from ..messaging.schemas import AnaliseMessage
from ..service.customer_service import CustomerService
from ..repository.transaction_repository import TransactionRepository
from ..schemas.transaction import TransactionCreate, TransactionResponse

class TransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        customer_service: CustomerService,
        producer: RabbitMQProducer
        #ml_service: ml_service,
    ):
        self.transaction_repo = transaction_repo
        self.customer_service = customer_service
        self.producer = producer
        

    async def process_transaction(self, transaction_data: TransactionCreate) -> TransactionResponse:
        if (transaction_data.amount < 0):
            raise ValueError("Transaction amount must be equal to or greater than 0.")

        existing = await self.transaction_repo.get_by_id(transaction_data.transaction_id)
        if existing:
            raise ValueError("Transaction ID already exists")
        
        customer = transaction_data.customer.model_dump()
        customer = await self.customer_service.get_by_id(customer["customer_id"])
        if customer is None:
            customer = await self.customer_service.create(transaction_data.customer)

        transaction = transaction_data.model_dump(exclude={"customer"})
        transaction["customer_id"] = customer.id

        db_transaction = await self.transaction_repo.create(transaction_data=transaction_data)

        await self.producer.publish(
            routing_key="transaction.analise",
            message=AnaliseMessage(
                transaction_id=db_transaction.id
            )
        )

        return TransactionResponse.model_validate(db_transaction)