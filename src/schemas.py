from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, UUID4, validator


class RegisterUser(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=4, max_length=16)


class ReadUser(BaseModel):
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class OrderItem(BaseModel):
    item_uuid: UUID4
    price: float = Field(gt=0)
    amount: int = Field(gt=0)


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


class RegisterOrder(BaseModel):
    items: list[OrderItem]
    
    @validator("items")
    def items_must_be_unique(cls, value):
        unique_values = len(set(item.item_uuid for item in value))
        if len(value) != unique_values:
            raise ValueError("Order items must be unique")
        return value


class ReadOrder(BaseModel):
    id: UUID4
    user_id: int
    items: list[OrderItem]
    total_price: float
    status: OrderStatus
    created_at: datetime


class PatchOrder(BaseModel):
    status: OrderStatus



