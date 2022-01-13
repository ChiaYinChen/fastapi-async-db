"""Pytest's conftest.py."""
from asyncio import get_event_loop
from typing import Dict, Generator

import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.main import app
from tests.utils.user import (authentication_token_from_email,
                              user_authentication_headers)


@pytest.fixture(scope="module")
async def client() -> Generator:
    """Mock async client."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop


@pytest.fixture(scope="module")
async def normal_user_token_headers(
    client: AsyncClient
) -> Dict[str, str]:
    """Token headers for normal user."""
    return await authentication_token_from_email(
        client=client,
        email=settings.TEST_USER_EMAIL
    )


@pytest.fixture(scope="module")
async def superuser_token_headers(
    client: AsyncClient
) -> Dict[str, str]:
    """Token headers for superuser."""
    return await user_authentication_headers(
        client=client,
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=settings.FIRST_SUPERUSER_PASSWORD
    )
