"""Initial db."""
import logging

from ..core.config import settings
from ..crud.crud_user import CRUDUser
from ..schemas.user import UserCreate

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """Initialize super user."""
    user = await CRUDUser.get_by_email(email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        logger.info('Initial Super User')
        await CRUDUser.create(obj_in=user_in)
    else:
        logger.warning(
            "Skipping creating superuser. User with email "
            f"`{settings.FIRST_SUPERUSER_EMAIL}` already exists. "
        )
