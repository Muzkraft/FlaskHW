from decimal import Decimal

from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    title: str = Field(..., title="title", min_length=2, max_length=64)
    description: str = Field(..., title="description", max_length=256)
    price: Decimal = Field(..., title="price", ge=0, description="Price of an item", quant_digits=2, decimal_places=2)


class Item(ItemIn):
    id: int
