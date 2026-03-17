from sqlalchemy.orm import Session

from retail_api.common.exceptions import NotFoundError
from retail_api.order.models import Order


def GetOrderForPayment(db: Session, order_id: str) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NotFoundError("Order not found", details={"order_id": order_id})
    return order


def MarkOrderPaid(db: Session, order_id: str) -> Order:
    order = GetOrderForPayment(db, order_id)
    order.status = "paid"
    db.commit()
    db.refresh(order)
    return order
