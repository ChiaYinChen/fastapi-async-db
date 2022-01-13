"""Crud user logic unit test."""
import pytest

from app.core.config import settings
from app.core.security import verify_password
from app.crud.crud_user import CRUDUser
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


@pytest.mark.asyncio
async def test_create_user() -> None:
    """Test for create user."""
    user = await CRUDUser.get_by_email(email=settings.TEST_USER_EMAIL)
    if user:
        await CRUDUser.remove(db_obj=user)
    user_in = UserCreate(
        email=settings.TEST_USER_EMAIL,
        password=settings.TEST_USER_PASSWORD
    )
    user = await CRUDUser.create(obj_in=user_in)
    assert user.email == settings.TEST_USER_EMAIL
    assert hasattr(user, "hashed_password")
    _test_check_if_user_is_active(db_obj=user)
    _test_check_if_user_is_superuser_normal_user(db_obj=user)


def _test_check_if_user_is_active(*, db_obj: UserModel) -> None:
    """Test for check if user is active."""
    is_active = CRUDUser.is_active(db_obj)
    assert is_active is True


def _test_check_if_user_is_superuser_normal_user(*, db_obj: UserModel) -> None:
    """Test for check if user is superuser (with normal user)."""
    is_superuser = CRUDUser.is_superuser(db_obj)
    assert is_superuser is False


@pytest.mark.asyncio
async def test_authenticate_user() -> None:
    """Test for authenticate user."""
    authenticated_user = await CRUDUser.authenticate(
        email=settings.TEST_USER_EMAIL,
        password=settings.TEST_USER_PASSWORD
    )
    assert authenticated_user
    assert settings.TEST_USER_EMAIL == authenticated_user.email


@pytest.mark.asyncio
async def test_authenticate_user_fail() -> None:
    """Test for user authentication failure."""
    user = await CRUDUser.authenticate(
        email="not_exist_user_email",
        password="not_exist_user_password"
    )
    assert user is None


@pytest.mark.asyncio
async def test_get_user() -> None:
    """Test for get user."""
    user = await CRUDUser.get_by_email(email=settings.TEST_USER_EMAIL)
    assert user
    assert user.email == settings.TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_update_user() -> None:
    """Test for update user."""
    user = await CRUDUser.get_by_email(email=settings.TEST_USER_EMAIL)
    new_password = "newtestuserpass"
    user_in_update = UserUpdate(password=new_password)
    await CRUDUser.update(db_obj=user, obj_in=user_in_update)
    user_2 = await CRUDUser.get_by_email(email=settings.TEST_USER_EMAIL)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
