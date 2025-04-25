from sqlalchemy import Column, String, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from processor.database import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Transaction(BaseModel):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
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
    operator_id = Column(String(36), ForeignKey("users.id"))
    operator_decision = Column(String(20))
    operator_decision_time = Column(DateTime(timezone=True))
    operator_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # items = relationship("TransactionItem", back_populates="transaction")
    # customer = relationship("Customer", back_populates="transactions")
    # operator = relationship("User", back_populates="transactions")


