from datetime import datetime
from pydantic import BaseModel, Field

class CustomerCreate(BaseModel):
    customer_id: str = Field(...)
    email: str = Field(..., max_length=255)
    phone: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    address: str = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    zip_code: str = Field(...)
    country: str = Field(...)
    device_id: str = Field(...)
    ip_address: str = Field(...)
    last_activity: datetime = Field(...)

class CustomerResponse(BaseModel):
    id: str = Field(...)
    email: str = Field(..., max_length=255)
    phone: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    address: str = Field(...)
    city: str = Field(...)
    state: str = Field(...)
    zip_code: str = Field(...)
    country: str = Field(...)
    device_id: str = Field(...)
    ip_address: str = Field(...)
    last_activity: datetime = Field(...)