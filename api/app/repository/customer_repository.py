from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.customer import Customer

class CustomerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, customer_id: str) -> Customer | None:
        stmt = select(Customer).filter_by(id=customer_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def create(self, customer_data: dict) -> Customer:
        customer_id = customer_data.pop("customer_id")

        db_customer = Customer(
            **customer_data,
            id = customer_id
        )

        self.db.add(db_customer)

        await self.db.commit()
        await self.db.refresh(db_customer)

        return db_customer
