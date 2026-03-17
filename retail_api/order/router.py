from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from retail_api.common.auth import GetCurrentUser
from retail_api.db.session import get_db
from retail_api.order.schemas import OrderCreateIn, OrderItemOut, OrderOut
from retail_api.order.service import CreateOrder, GetOrderById
from retail_api.user.models import User

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def OrderCreate(
    body: OrderCreateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(GetCurrentUser),
):
    from retail_api.order.models import OrderItem

    order = CreateOrder(db, current_user.id, body)
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status,
        items=[
            OrderItemOut(
                product_id=oi.product_id,
                quantity=oi.quantity,
                price_snapshot=oi.price_snapshot,
            )
            for oi in order_items
        ],
    )


@router.get("/{order_id}", response_model=OrderOut)
def OrderGet(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(GetCurrentUser),
):
    from retail_api.order.models import OrderItem

    order = GetOrderById(db, order_id, current_user.id)
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status,
        items=[
            OrderItemOut(
                product_id=oi.product_id,
                quantity=oi.quantity,
                price_snapshot=oi.price_snapshot,
            )
            for oi in order_items
        ],
    )
