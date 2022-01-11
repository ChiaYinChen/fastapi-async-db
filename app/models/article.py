"""Database ORM models for article."""
from datetime import datetime

import ormar
from sqlalchemy import func

from ..models.base import BaseMeta
from ..models.user import User


class Post(ormar.Model):
    """Table for post."""

    class Meta(BaseMeta):
        tablename = "post"

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    title: str = ormar.String(max_length=200)
    author: User = ormar.ForeignKey(
        User, related_name="post",
        onupdate="CASCADE", ondelete="CASCADE"
    )
    created_time: datetime = ormar.DateTime(server_default=func.now())
