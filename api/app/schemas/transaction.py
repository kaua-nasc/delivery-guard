from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

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
    product_name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    category: Optional[str] = Field(None, max_length=50)

class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., min_length=1, max_length=50)
    customer_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    payment_method: PaymentMethod
    card_last_four: Optional[str] = Field(None, min_length=4, max_length=4)
    card_brand: Optional[str] = Field(None, max_length=20)
    billing_address: Optional[str]
    shipping_address: Optional[str]
    ip_address: Optional[str] = Field(None, max_length=50)
    device_id: Optional[str] = Field(None, max_length=100)
    items: List[TransactionItemCreate]
    currency: str = Field("BRL", min_length=3, max_length=3)

    @field_validator('card_last_four')
    def validate_card_last_four(cls, v, values):
        if 'payment_method' in values and values['payment_method'] in ['credit_card', 'debit_card'] and not v:
            raise ValueError('card_last_four is required for card payments')
        return v

class TransactionResponse(BaseModel):
    id: int
    transaction_id: str
    customer_id: int
    amount: float
    currency: str
    payment_method: str
    card_last_four: Optional[str]
    card_brand: Optional[str]
    status: str
    ml_status: Optional[str]
    ml_score: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus]
    operator_notes: Optional[str] = Field(None, max_length=500)