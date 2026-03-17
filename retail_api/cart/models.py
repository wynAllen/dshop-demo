from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import DateTime

from retail_api.db.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(String(36), primary_key=True)
    cart_id = Column(String(64), nullable=False, index=True)
    product_id = Column(String(36), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
