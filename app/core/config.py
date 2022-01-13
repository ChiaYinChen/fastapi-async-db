"""Settings."""
import logging.config
from os.path import abspath, dirname, join

from pydantic import BaseSettings


class Settings(BaseSettings):

    SECRET_KEY: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./prod.db"

    TESTING: bool = False
    TEST_SQLALCHEMY_DATABASE_URI: str = "sqlite:///./test.db"
    TEST_USER_EMAIL: str = "test@example.com"
    TEST_USER_PASSWORD: str = "testuserpass"
    FIRST_SUPERUSER_EMAIL: str = "testsuper@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "superuserpass"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# logging setting
PROJ_ROOT = dirname(dirname(dirname(abspath(__file__))))
LOG_FILE_PATH = join(PROJ_ROOT, "app", "logging.conf")
logging.config.fileConfig(LOG_FILE_PATH)
