from pydantic import BaseModel, Field
from datetime import date

from sqlalchemy import Enum


class OrderStatus(str, Enum):
    accepted = "accepted"
    processing = "processing"
    shipped = "shipped"


class OrderIn(BaseModel):
    status: str = Field(default="created")


class Order(BaseModel):
    id: int
    user_id: int = Field(..., title="User id")
    item_id: int = Field(..., title="Item id")
    order_date: date = Field(..., title="Order date", description="YYYY-MM-DD")
    status: str = Field(default="created")

    class Config:
        from_attributes = True
