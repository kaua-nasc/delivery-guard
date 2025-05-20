from __future__ import annotations
from sqlalchemy import String, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from ..models.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="BRL")
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    card_last_four: Mapped[str | None] = mapped_column(String(4), nullable=True)
    card_brand: Mapped[str | None] = mapped_column(String(20), nullable=True)
    billing_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    shipping_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    ml_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ml_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    ml_decision_time: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    operator_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    operator_decision: Mapped[str | None] = mapped_column(String(20), nullable=True)
    operator_decision_time: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    operator_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

transaction_items  = relationship("api.app.models.transaction_item.TransactionItem", back_populates="transaction")
customer = relationship("Customer", back_populates="transactions")
operator = relationship("User", back_populates="transactions")