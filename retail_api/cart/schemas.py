from typing import List

from pydantic import BaseModel


class CartItemIn(BaseModel):
    product_id: str
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: str
    product_id: str
    quantity: int

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    items: List[CartItemOut]
