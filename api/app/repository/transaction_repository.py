from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.transaction import Transaction
from ..models.transaction_item import TransactionItem

class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, transaction_id: str) -> Transaction | None:
        stmt = select(Transaction).filter_by(id=transaction_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def create(self, transaction_data: dict) -> Transaction:
        items_data = transaction_data.pop("items", [])
        
        transaction_id = transaction_data.pop("transaction_id")
        db_transaction = Transaction(
            **transaction_data,
            id = transaction_id
        )
        self.db.add(db_transaction)
        await self.db.flush()
        
        items = []
        for item_data in items_data:
            items.append(TransactionItem(
                **item_data,
                transaction_id=db_transaction.id
            ))
        self.db.add_all(items)
        
        await self.db.commit()
        await self.db.refresh(db_transaction)
        return db_transaction
    
    def update_status(self, transaction_id: str, status: str) -> Transaction:
        transaction = self.get_by_id(transaction_id)
        if not transaction: 
            raise ValueError("Transaction not found")

        transaction.status = status
        self.db.commit()
        self.db.refresh(transaction)
        return transaction