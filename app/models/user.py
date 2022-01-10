"""Database ORM models for user."""
from datetime import datetime

import ormar
from sqlalchemy import func
from sqlalchemy.sql import expression

from ..models.base import BaseMeta


class User(ormar.Model):
    """Table for user."""

    class Meta(BaseMeta):
        tablename = "user"

    user_id: int = ormar.Integer(primary_key=True, autoincrement=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False, index=True)  # noqa: E501
    hashed_password: str = ormar.String(max_length=255, nullable=False, name="password")  # noqa: E501
    full_name: str = ormar.String(max_length=64, nullable=True)
    created_time: datetime = ormar.DateTime(server_default=func.now())
    is_active: bool = ormar.Boolean(server_default=expression.true(), default=True)  # noqa: E501
    is_superuser: bool = ormar.Boolean(server_default=expression.false(), default=False)  # noqa: E501
