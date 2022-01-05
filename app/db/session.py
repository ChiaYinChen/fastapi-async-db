from databases import Database
from sqlalchemy import create_engine

# databases query builder
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
database = Database(SQLALCHEMY_DATABASE_URL)

# SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
