"""Pytest's conftest.py."""
import logging
from asyncio import get_event_loop
from typing import Dict, Generator

import pytest
from httpx import AsyncClient

from app import color_formatter
from app.core.config import settings
from app.main import app
from tests.utils.user import authentication_token_from_email


@pytest.fixture(scope="module")
async def client() -> Generator:
    """Mock async client."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop


@pytest.fixture(scope="module", autouse=True)
async def normal_user_token_headers(
    client: AsyncClient
) -> Dict[str, str]:
    """Token headers for normal user."""
    return await authentication_token_from_email(
        client=client,
        email=settings.TEST_USER_EMAIL,
        password=settings.TEST_USER_PASSWORD
    )


@pytest.fixture(scope="module", autouse=True)
async def superuser_token_headers(
    client: AsyncClient
) -> Dict[str, str]:
    """Token headers for superuser."""
    return await authentication_token_from_email(
        client=client,
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        superuser=True
    )


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Set custom logging handler for pytest."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    _handler = logging.StreamHandler()
    _handler.setFormatter(color_formatter)
    logger.addHandler(_handler)
