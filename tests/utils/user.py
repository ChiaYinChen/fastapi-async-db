"""Util function for unit test."""
from typing import Dict

from httpx import AsyncClient

from app.core.config import settings
from app.crud.crud_user import CRUDUser
from app.schemas.user import UserCreate, UserUpdate


async def user_authentication_headers(
    client: AsyncClient, email: str, password: str
) -> Dict[str, str]:
    """Obtain user access_token."""
    data = {"username": email, "password": password}
    resp = await client.post("/login/access-token", data=data)
    response = resp.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def authentication_token_from_email(
    client: AsyncClient, email: str, password: str, superuser: bool = False
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    # password = settings.TEST_USER_PASSWORD
    db_user = await CRUDUser.get_by_email(email=email)
    if not db_user:
        user_in_create = UserCreate(email=email, password=password, is_superuser=superuser)  # noqa: E501
        await CRUDUser.create(obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password, is_superuser=superuser)
        await CRUDUser.update(db_obj=db_user, obj_in=user_in_update)

    return await user_authentication_headers(client=client, email=email, password=password)  # noqa: E501
