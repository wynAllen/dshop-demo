from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from retail_api.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    total_amount = Column(Float, nullable=False)
    status = Column(String(32), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String(36), primary_key=True)
    order_id = Column(String(36), nullable=False, index=True)
    product_id = Column(String(36), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_snapshot = Column(Float, nullable=False)
