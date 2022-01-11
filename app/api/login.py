"""Router for login."""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..core.security import create_access_token
from ..crud.crud_user import CRUDUser
from ..dependencies import get_current_user
from ..models.user import User as UserModel
from ..schemas.token import Token
from ..schemas.user import User

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await CRUDUser.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")  # noqa: E501
    return {
        "access_token": create_access_token(sub=user.email),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=User)
async def test_token(
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    Test access token.
    """
    return current_user
