from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from retail_api.common.exceptions import AppException
from retail_api.config import settings
from retail_api.db.session import get_db
from retail_api.user.models import User

security = HTTPBearer(auto_error=False)


def CreateAccessToken(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode["exp"] = expire
    return jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )


def GetCurrentUser(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> User:
    if not credentials or credentials.credentials is None:
        raise AppException(
            message="Not authenticated",
            code="UNAUTHORIZED",
            status_code=401,
        )
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise AppException(
                message="Invalid token",
                code="UNAUTHORIZED",
                status_code=401,
            )
    except JWTError:
        raise AppException(
            message="Invalid or expired token",
            code="UNAUTHORIZED",
            status_code=401,
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AppException(
            message="User not found",
            code="UNAUTHORIZED",
            status_code=401,
        )
    return user
