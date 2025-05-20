from __future__ import annotations
from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..models.base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    email: Mapped[str | None] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(20))
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(50))
    state: Mapped[str | None] = mapped_column(String(50))
    zip_code: Mapped[str | None] = mapped_column(String(20))
    country: Mapped[str | None] = mapped_column(String(50))
    device_id: Mapped[str | None] = mapped_column(String(100))
    ip_address: Mapped[str | None] = mapped_column(String(50))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    risk_score: Mapped[int] = mapped_column(Integer, default=0)
    last_activity: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

transactions = relationship("Transaction", back_populates="customer")