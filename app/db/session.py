from databases import Database
from sqlalchemy import create_engine, MetaData

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
database = Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True
)
