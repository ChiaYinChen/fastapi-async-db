"""Login unit test."""
from typing import Dict

import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def test_get_access_token(
    client: AsyncClient
) -> None:
    """Test output format for `/login/access-token` endpoint."""
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    resp = await client.post("/login/access-token", data=login_data)
    tokens = resp.json()
    assert resp.status_code == 200
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_use_access_token(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str]
) -> None:
    """Test output format for `/login/test-token` endpoint."""
    resp = await client.post("/login/test-token", headers=superuser_token_headers)  # noqa: E501
    result = resp.json()
    assert resp.status_code == 200
    assert isinstance(result, dict)
    assert "user_id" in result
