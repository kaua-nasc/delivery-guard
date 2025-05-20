import decimal
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
from .customer import CustomerCreate

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PIX = "pix"
    BANK_TRANSFER = "bank_transfer"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    REFUNDED = "refunded"

class MLStatus(str, Enum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    FRAUDULENT = "fraudulent"
    PENDING = "pending"
    ERROR = "error"


class TransactionItemCreate(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: decimal.Decimal
    category: str

class TransactionItemResponse(BaseModel):
    product_id: str
    # product_name: str
    # quantity: int
    # unit_price: decimal.Decimal
    # category: str
    

class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=50)
    amount: decimal.Decimal = Field(..., ge=0)
    payment_method: PaymentMethod
    card_last_four: Optional[str] = Field(None, min_length=4, max_length=4)
    card_brand: Optional[str] = Field(None, max_length=20)
    billing_address: Optional[str]
    shipping_address: Optional[str]
    ip_address: Optional[str] = Field(None, max_length=50)
    device_id: Optional[str] = Field(None, max_length=100)
    customer: CustomerCreate
    items: List[TransactionItemCreate]
    currency: Optional[str] = Field(default="BRL", min_length=3, max_length=3)

    @field_validator('card_last_four')
    def validate_card_last_four(cls, v: Optional[str], info: ValidationInfo):
        data = info.data
        payment_method = data.get('payment_method')
        
        if payment_method in ['credit_card', 'debit_card'] and not v:
            raise ValueError('card_last_four is required for card payments')
        return v

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_id: str
    amount: decimal.Decimal
    status: Optional[str] = None
    ml_status: Optional[str] = None
    ml_score: Optional[decimal.Decimal] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus]
    operator_notes: Optional[str] = Field(None, max_length=500)