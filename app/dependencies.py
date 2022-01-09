"""Dependencies."""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from .core.config import settings
from .crud.crud_user import CRUDUser
from .models.user import user as UserModel
from .schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="login/access-token")


async def get_current_user(
    token: str = Depends(reusable_oauth2)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )
    user = await CRUDUser.get_by_email(email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user)
):
    if not CRUDUser.is_active(current_user):
        raise HTTPException(status_code=401, detail="Inactive user")
    return current_user
