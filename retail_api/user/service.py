import uuid

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from retail_api.common.exceptions import AppException
from retail_api.user.models import User
from retail_api.user.schemas import RegisterIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def CreateUser(db: Session, data: RegisterIn) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise AppException(
            message="Email already registered",
            code="CONFLICT",
            status_code=409,
        )
    user = User(
        id=uuid.uuid4().hex,
        email=data.email,
        hashed_password=pwd_context.hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def AuthenticateUser(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user
