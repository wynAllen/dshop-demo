from typing import List, Optional

from pydantic import BaseModel


class ProductOut(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        from_attributes = True


class ProductListOut(BaseModel):
    items: List[ProductOut]
    total: int
    page: int
