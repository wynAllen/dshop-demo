from typing import Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from retail_api.common.auth import GetCurrentUserOptional
from retail_api.db.session import get_db
from retail_api.user.models import User
from retail_api.cart.schemas import CartItemIn, CartItemOut, CartItemUpdate, CartOut
from retail_api.cart.service import (
    AddCartItem,
    GetCart,
    GetCartId,
    RemoveCartItem,
    UpdateCartItem,
)

router = APIRouter(prefix="/api/v1/cart", tags=["cart"])


def _cart_id(
    x_cart_id: Optional[str] = Header(None, alias="X-Cart-Id"),
    current_user: Optional[User] = Depends(GetCurrentUserOptional),
) -> str:
    user_id = current_user.id if current_user else None
    return GetCartId(user_id, x_cart_id)


@router.get("", response_model=CartOut)
def CartGet(
    db: Session = Depends(get_db),
    cart_id: str = Depends(_cart_id),
):
    items = GetCart(db, cart_id)
    return CartOut(items=[CartItemOut.model_validate(i) for i in items])


@router.post("/items", response_model=CartItemOut)
def CartAddItem(
    body: CartItemIn,
    db: Session = Depends(get_db),
    cart_id: str = Depends(_cart_id),
):
    item = AddCartItem(db, cart_id, body.product_id, body.quantity)
    return CartItemOut.model_validate(item)


@router.patch("/items/{item_id}", response_model=CartItemOut)
def CartUpdateItem(
    item_id: str,
    body: CartItemUpdate,
    db: Session = Depends(get_db),
    cart_id: str = Depends(_cart_id),
):
    item = UpdateCartItem(db, cart_id, item_id, body.quantity)
    return CartItemOut.model_validate(item)


@router.delete("/items/{item_id}")
def CartDeleteItem(
    item_id: str,
    db: Session = Depends(get_db),
    cart_id: str = Depends(_cart_id),
):
    RemoveCartItem(db, cart_id, item_id)
    return {}
