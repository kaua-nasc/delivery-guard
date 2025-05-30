from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.transaction import Transaction
from ..models.transaction_item import TransactionItem
from ..schemas import transaction as schemas

class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, transaction_id: str) -> Transaction | None:
        stmt = select(Transaction).filter_by(id=transaction_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def create(self, transaction_data: schemas.TransactionCreate) -> Transaction:
        db_transaction = Transaction(
            id = transaction_data.transaction_id,
            customer_id = transaction_data.customer.customer_id,
            amount = transaction_data.amount,
            currency = transaction_data.currency,
            payment_method = transaction_data.payment_method,
            card_last_four = transaction_data.card_last_four,
            card_brand = transaction_data.card_brand,
            billing_address = transaction_data.billing_address,
            shipping_address = transaction_data.shipping_address,
            ip_address = transaction_data.ip_address,
            device_id = transaction_data.device_id,
            status = None,
            ml_status = None,
            ml_score = None,
            ml_decision_time = None,
            operator_id = None,
            operator_decision = None,
            operator_decision_time = None,
            operator_notes = None,
            created_at = None,
            updated_at = None,
        )
        self.db.add(db_transaction)
        await self.db.flush()
        
        items = [
            TransactionItem(
                transaction_id=db_transaction.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                category=item.category,
                created_at=None,
            )
            for item in transaction_data.items
        ]
        self.db.add_all(items)
        
        await self.db.commit()
        await self.db.refresh(db_transaction)
        return db_transaction

    async def update_status(self, transaction_id: str, status: str) -> Transaction:
        transaction = await self.get_by_id(transaction_id)
        if not transaction: 
            raise ValueError("Transaction not found")
        transaction.status = status
        await self.db.commit()
        await self.db.refresh(transaction)
        return transaction