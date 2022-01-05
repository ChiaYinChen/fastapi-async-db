"""Database ORM models for user."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table
from sqlalchemy.sql import expression

from ..db.base_class import metadata

user = Table(
    "user",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(256), unique=True, nullable=False, index=True),
    Column("hashed_password", String, nullable=False),
    Column("full_name", String(64), nullable=True),
    Column("created_time", DateTime, nullable=False, default=datetime.now),
    Column("is_active", Boolean, server_default=expression.true(), default=True),  # noqa: E501
    Column("is_superuser", Boolean, server_default=expression.false(), default=False)  # noqa: E501
)
