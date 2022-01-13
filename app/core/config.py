"""Settings."""
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

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
