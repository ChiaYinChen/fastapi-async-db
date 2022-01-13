"""User unit test."""
import logging
from typing import Dict

import pytest
from httpx import AsyncClient

from app.core.config import settings

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_get_user_me_by_normal(
    client: AsyncClient,
    normal_user_token_headers: Dict[str, str]
) -> None:
    """Test get_user_me with normal user."""
    resp = await client.get("/users/me", headers=normal_user_token_headers)
    current_user = resp.json()
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_get_user_me_by_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str]
) -> None:
    """Test get_user_me with superuser."""
    resp = await client.get("/users/me", headers=superuser_token_headers)
    current_user = resp.json()
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.FIRST_SUPERUSER_EMAIL


@pytest.mark.asyncio
async def test_get_users_by_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str]
) -> None:
    """Test get_users with superuser."""
    resp = await client.get("/users/?skip=0&limit=100", headers=superuser_token_headers)  # noqa: E501
    all_users = resp.json()
    logger.debug(f"Total get {len(all_users)} users.")
    assert resp.status_code == 200
    assert isinstance(all_users, list)
    assert len(all_users) > 0


@pytest.mark.asyncio
async def test_get_users_by_normal(
    client: AsyncClient,
    normal_user_token_headers: Dict[str, str]
) -> None:
    """Test get_users with normal user."""
    resp = await client.get("/users/?skip=0&limit=100", headers=normal_user_token_headers)  # noqa: E501
    all_users = resp.json()
    assert resp.status_code == 401
    assert all_users == {"detail": "The user doesn't have enough privileges"}


@pytest.mark.asyncio
async def test_get_user(
    client: AsyncClient
) -> None:
    """Test get_user (existing user)."""
    resp = await client.get(f"/users/{settings.TEST_USER_EMAIL}")
    api_user = resp.json()
    assert resp.status_code == 200
    assert isinstance(api_user, dict)
    assert api_user["email"] == settings.TEST_USER_EMAIL


@pytest.mark.asyncio
async def test_get_user_not_exist(
    client: AsyncClient
) -> None:
    """Test get_user (user not exist)."""
    resp = await client.get("/users/not_exist_user_email")
    api_user = resp.json()
    assert resp.status_code == 404
    assert api_user == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_create_exist_user(
    client: AsyncClient
) -> None:
    """Test create_user (existing user)."""
    data = {
        "email": settings.TEST_USER_EMAIL,
        "password": settings.TEST_USER_PASSWORD
    }
    resp = await client.post("/users/", json=data)
    created_user = resp.json()
    assert resp.status_code == 400
    assert created_user == {"message": "User already exist"}


@pytest.mark.asyncio
async def test_update_user_not_exist(
    client: AsyncClient
) -> None:
    """Test update_user (user not exist)."""
    data = {"email": "not_found@example.com"}
    resp = await client.patch("/users/not_exist_user_email", json=data)
    created_user = resp.json()
    assert resp.status_code == 404
    assert created_user == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_delete_user_not_exist(
    client: AsyncClient
) -> None:
    """Test delete_user (user not exist)."""
    resp = await client.delete("/users/not_exist_user")
    created_user = resp.json()
    assert resp.status_code == 404
    assert created_user == {"detail": "User not found"}
