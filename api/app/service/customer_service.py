from ..repository.customer_repository import CustomerRepository
from ..schemas.customer import CustomerCreate, CustomerResponse

class CustomerService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    async def get_by_id(self, customer_id: str) -> CustomerResponse | None:
        return await self.customer_repo.get_by_id(customer_id)

    async def create(self, customer_data: CustomerCreate) -> CustomerResponse:
        fields_to_check = {
            "email": customer_data.email,
            "phone": customer_data.phone,
            "first_name": customer_data.first_name,
            "last_name": customer_data.last_name,
            "ip_address": customer_data.ip_address,
        }

        for field, value in fields_to_check.items():
            if value and await self.customer_repo.exists_by_fields({field: value}):
                raise ValueError(f"O campo {field} com valor {value} já está em uso")


        db_customer = await self.customer_repo.create({**customer_data.model_dump()})

        return CustomerResponse.model_validate(db_customer)
