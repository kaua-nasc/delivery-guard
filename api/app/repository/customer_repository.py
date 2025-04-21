from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.customer import Customer

class CustomerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, customer_id: str) -> Customer | None:
        stmt = select(Customer).filter_by(id=customer_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    

    async def exists_by_fields(self, fields: dict) -> bool:
        if not fields:
            return False

        conditions = [getattr(Customer, field) == value for field, value in fields.items()]
        stmt = select(Customer).where(and_(*conditions)).limit(1)
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None

    
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
