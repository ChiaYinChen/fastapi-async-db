"""Initial data."""
import asyncio
import logging

from app.db.init_db import init_db
from app.db.session import database

logger = logging.getLogger(__name__)


async def init() -> None:
    """Initialize database."""
    async with database:
        await init_db()


def main() -> None:
    """Execute."""
    logger.info("Creating initial data")
    asyncio.run(init())
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
