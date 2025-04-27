from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .schema import Transaction


async def process_transaction(message: dict):
    print(message)

    async with get_db() as db:
        transaction = await db.execute(select(Transaction).filter_by(id=message["transaction_id"]))

        transaction = transaction.scalar()

        # manda pra IA
        # codigo q manda pra IA deve ser aq

        if transaction:
            await db.execute(update(Transaction).where(Transaction.id == transaction.id).values(status="processed"))
            await db.commit()