from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from retail_api.common.auth import GetCurrentUser
from retail_api.common.exceptions import AppException
from retail_api.db.session import get_db
from retail_api.user.models import User
from retail_api.user.schemas import LoginIn, RegisterIn, TokenOut, UserOut
from retail_api.user.service import AuthenticateUser, CreateUser

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def Register(db: Session = Depends(get_db), body: RegisterIn = ...):
    user = CreateUser(db, body)
    return UserOut(id=user.id, email=user.email)


@router.post("/login", response_model=TokenOut)
def Login(db: Session = Depends(get_db), body: LoginIn = ...):
    user = AuthenticateUser(db, body.email, body.password)
    if not user:
        raise AppException(
            message="Invalid email or password",
            code="UNAUTHORIZED",
            status_code=401,
        )
    from retail_api.common.auth import CreateAccessToken

    token = CreateAccessToken({"sub": user.id})
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserOut)
def Me(current_user: User = Depends(GetCurrentUser)):
    return UserOut(id=current_user.id, email=current_user.email)
