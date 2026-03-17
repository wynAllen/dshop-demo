from typing import List

from pydantic import BaseModel


class OrderItemIn(BaseModel):
    product_id: str
    quantity: int


class OrderCreateIn(BaseModel):
    items: List[OrderItemIn]


class OrderItemOut(BaseModel):
    product_id: str
    quantity: int
    price_snapshot: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: str
    user_id: str
    total_amount: float
    status: str
    items: List[OrderItemOut]
