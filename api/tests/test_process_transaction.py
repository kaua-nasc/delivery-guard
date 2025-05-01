from unittest.mock import AsyncMock, MagicMock
from api.app.models.transaction import Transaction
from api.app.schemas.customer import CustomerCreate
from api.app.schemas.transaction import TransactionCreate, TransactionItemCreate, TransactionResponse
from api.app.schemas.transaction import TransactionCreate
from api.app.service.transaction_service import TransactionService
from api.app.models import customer, transaction, user, transaction_item 
import pytest
from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_process_transaction_success():

    transaction_data = TransactionCreate(
        transaction_id="txn_001",
        amount=199.99,
        payment_method="credit_card",
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
                unit_price=79.99,
                category="Roupas"
            ),
            TransactionItemCreate(
                product_id="prod_002",
                product_name="Tênis Esportivo",
                quantity=1,
                unit_price=119.99,
                category="Calçados"
            )
        ],
        currency="BRL"
    )


    transaction_repo = MagicMock()
    transaction_repo.get_by_id = AsyncMock(return_value=None)
    transaction_repo.create = AsyncMock(return_value=Transaction(
        id=transaction_data.transaction_id,
        customer_id=transaction_data.customer.customer_id,
        amount=transaction_data.amount,
        currency=transaction_data.currency,
        payment_method=str(transaction_data.payment_method),
        card_last_four=transaction_data.card_last_four,
        card_brand=transaction_data.card_brand,
        billing_address=transaction_data.billing_address,
        shipping_address=transaction_data.shipping_address,
        ip_address=transaction_data.ip_address,
        device_id=transaction_data.device_id,
        status=None,
        ml_status=None,
        ml_score=None,
        ml_decision_time=None,
        operator_id=None,
        operator_decision=None,
        operator_decision_time=None,
        operator_notes=None,
        created_at=None,
        updated_at=None,
    ))

    customer_service = MagicMock()
    customer_service.get_by_id = AsyncMock(return_value=None)
    customer_service.create = AsyncMock(return_value=MagicMock(id='c001'))

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