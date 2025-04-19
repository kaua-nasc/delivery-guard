from ..repository.customer_repository import CustomerRepository
from ..schemas.customer import CustomerCreate, CustomerResponse

class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def get_by_id(self, customer_id: str) -> CustomerResponse | None:
        return await self.customer_repo.get_by_id(customer_id)

    async def create(self, customer_data: CustomerCreate) -> CustomerResponse:
        db_customer = await self.customer_repo.create({**customer_data})

        return CustomerResponse.model_validate(db_customer)
