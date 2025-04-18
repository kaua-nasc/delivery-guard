from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..models.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="BRL")
    payment_method = Column(String(50), nullable=False)
    card_last_four = Column(String(4))
    card_brand = Column(String(20))
    billing_address = Column(Text)
    shipping_address = Column(Text)
    ip_address = Column(String(50))
    device_id = Column(String(100))
    status = Column(String(20), default="pending")
    ml_status = Column(String(20))
    ml_score = Column(Numeric(5, 4))
    ml_decision_time = Column(DateTime(timezone=True))
    operator_id = Column(Integer, ForeignKey("users.id"))
    operator_decision = Column(String(20))
    operator_decision_time = Column(DateTime(timezone=True))
    operator_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("TransactionItem", back_populates="transaction")
    customer = relationship("Customer", back_populates="transactions")

