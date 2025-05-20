from datetime import datetime, timezone
import decimal
from unittest.mock import AsyncMock, MagicMock

from api.app.schemas.customer import CustomerCreate
from api.app.schemas.transaction import PaymentMethod, TransactionCreate, TransactionItemCreate, TransactionResponse
from api.app.service.transaction_service import TransactionService
import pytest
from . import mocks
from api.app.models import * 


@pytest.mark.asyncio
async def test_process_transaction_success():
    transaction_data = mocks.transaction_correct_input

    transaction_repo = MagicMock()
    transaction_repo.get_by_id = AsyncMock(return_value=None)
    transaction_repo.create = AsyncMock(return_value=mocks.transaction_correct_created)

    customer_service = MagicMock()
    customer_service.get_by_id = AsyncMock(return_value=None)
    customer_service.create = AsyncMock(return_value=MagicMock(**mocks.transaction_response_correct_created.model_dump()))

    producer = MagicMock()
    producer.publish = AsyncMock()

    service = TransactionService(
        transaction_repo=transaction_repo,
        customer_service=customer_service,
        producer=producer
    )

    result = await service.process_transaction(transaction_data)

    assert isinstance(result, TransactionResponse)
    assert result.id == 'txn_001'
    transaction_repo.get_by_id.assert_awaited_once()
    transaction_repo.create.assert_awaited_once()
    customer_service.get_by_id.assert_awaited_once()
    customer_service.create.assert_awaited_once()
    producer.publish.assert_awaited_once()

@pytest.mark.asyncio
async def test_transaction_invalid_amount():
    with pytest.raises(ValueError):
        TransactionCreate(
            transaction_id="txn_001",
            amount=decimal.Decimal(-9.92),
            payment_method=PaymentMethod.CREDIT_CARD,
            card_last_four="1234",
            card_brand="Visa",
            billing_address="Rua A, 123",
            shipping_address="Rua B, 456",
            ip_address="192.168.0.1",
            device_id="device-abc-123",
            customer=CustomerCreate(
                customer_id="cust_001",
                email="johndoe@example.com",
                phone="+5511999999999",
                first_name="John",
                last_name="Doe",
                address="Rua X, 123",
                city="São Paulo",
                state="SP",
                zip_code="01234-567",
                country="BR",
                device_id="device-abc-123",
                ip_address="192.168.0.1",
                last_activity=datetime.now(timezone.utc)
            ),
            items=[
                TransactionItemCreate(
                    product_id="prod_001",
                    product_name="Camisa Polo",
                    quantity=2,
                    unit_price=decimal.Decimal(79.99),
                    category="Roupas"
                ),
                TransactionItemCreate(
                    product_id="prod_002",
                    product_name="Tênis Esportivo",
                    quantity=1,
                    unit_price=decimal.Decimal(119.99),
                    category="Calçados"
                )
            ],
            currency="BRL"
        )
