"""Pytest's conftest.py."""
from asyncio import get_event_loop
from typing import Generator

import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="module")
async def client() -> Generator:
    """Mock async client."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()
    yield loop
