"""DB Session."""
from databases import Database
from sqlalchemy import create_engine, MetaData

from ..core.config import settings

if settings.TESTING:
    database = Database(settings.TEST_SQLALCHEMY_DATABASE_URI, force_rollback=True)  # noqa: E501
else:
    database = Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True
)
