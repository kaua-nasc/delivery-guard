from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, Text

from ..models.base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"

    customer_id = Column(String(50), unique=True, nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    first_name = Column(String(50))
    last_name = Column(String(50))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    country = Column(String(50))
    device_id = Column(String(100))
    ip_address = Column(String(50))
    is_verified = Column(Boolean, default=False)
    risk_score = Column(Integer, default=0)
    last_activity = Column(TIMESTAMP(timezone=True))