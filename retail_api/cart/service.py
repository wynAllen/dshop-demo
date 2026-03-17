import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from retail_api.cart.models import CartItem
from retail_api.common.exceptions import NotFoundError


def GetCartId(user_id: Optional[str], cart_id_header: Optional[str]) -> str:
    if user_id:
        return f"user:{user_id}"
    return cart_id_header or f"anon:{uuid.uuid4().hex}"


def GetCart(db: Session, cart_id: str) -> List[CartItem]:
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()


def AddCartItem(
    db: Session,
    cart_id: str,
    product_id: str,
    quantity: int = 1,
) -> CartItem:
    existing = (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
        .first()
    )
    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing
    item = CartItem(
        id=uuid.uuid4().hex,
        cart_id=cart_id,
        product_id=product_id,
        quantity=quantity,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def UpdateCartItem(
    db: Session,
    cart_id: str,
    item_id: str,
    quantity: int,
) -> CartItem:
    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart_id)
        .first()
    )
    if not item:
        raise NotFoundError("Cart item not found", details={"item_id": item_id})
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def RemoveCartItem(db: Session, cart_id: str, item_id: str) -> None:
    item = (
        db.query(CartItem)
        .filter(CartItem.id == item_id, CartItem.cart_id == cart_id)
        .first()
    )
    if item:
        db.delete(item)
        db.commit()
