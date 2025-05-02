from datetime import datetime, timezone
from api.app.models.transaction import Transaction
from api.app.schemas.customer import CustomerCreate
from api.app.schemas.transaction import TransactionCreate, TransactionItemCreate, TransactionResponse


transaction_correct_input = TransactionCreate(
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

transaction_correct_created = Transaction(
    id=transaction_correct_input.transaction_id,
    customer_id=transaction_correct_input.customer.customer_id,
    amount=transaction_correct_input.amount,
    currency=transaction_correct_input.currency,
    payment_method=str(transaction_correct_input.payment_method),
    card_last_four=transaction_correct_input.card_last_four,
    card_brand=transaction_correct_input.card_brand,
    billing_address=transaction_correct_input.billing_address,
    shipping_address=transaction_correct_input.shipping_address,
    ip_address=transaction_correct_input.ip_address,
    device_id=transaction_correct_input.device_id,
    status="pending",
    ml_status=None,
    ml_score=None,
    ml_decision_time=None,
    operator_id=None,
    operator_decision=None,
    operator_decision_time=None,
    operator_notes=None,
    created_at=datetime.now(timezone.utc),
    updated_at=None,
)

transaction_response_correct_created = TransactionResponse(
    id=transaction_correct_input.transaction_id,
    customer_id=transaction_correct_input.customer.customer_id,
    amount=transaction_correct_input.amount,
    status="pending",
    ml_status=None,
    ml_score=None,
    created_at=transaction_correct_created.created_at,
    updated_at=None,
)