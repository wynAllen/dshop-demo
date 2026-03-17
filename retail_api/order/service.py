import uuid

from sqlalchemy.orm import Session

from retail_api.common.exceptions import NotFoundError
from retail_api.inventory.service import ReleaseStock, ReserveStock
from retail_api.order.models import Order, OrderItem
from retail_api.order.schemas import OrderCreateIn, OrderItemIn
from retail_api.product.models import Product


def CreateOrder(db: Session, user_id: str, body: OrderCreateIn) -> Order:
    order_id = uuid.uuid4().hex
    total = 0.0
    item_prices = []
    try:
        for it in body.items:
            price = ReserveStock(db, it.product_id, it.quantity)
            total += price * it.quantity
            item_prices.append((it.product_id, it.quantity, price))
        order = Order(
            id=order_id,
            user_id=user_id,
            total_amount=round(total, 2),
            status="pending",
        )
        db.add(order)
        for product_id, quantity, price in item_prices:
            db.add(
                OrderItem(
                    id=uuid.uuid4().hex,
                    order_id=order_id,
                    product_id=product_id,
                    quantity=quantity,
                    price_snapshot=price,
                )
            )
        db.commit()
        db.refresh(order)
        return order
    except Exception:
        for product_id, quantity, _ in item_prices:
            ReleaseStock(db, product_id, quantity)
        db.rollback()
        raise


def GetOrderById(db: Session, order_id: str, user_id: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise NotFoundError("Order not found", details={"order_id": order_id})
    return order
