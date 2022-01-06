"""CRUD for user."""
from typing import Any, Dict, Union

from ..core.security import get_password_hash, verify_password
from ..db.session import database
from ..models.user import user as UserModel
from ..schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser:

    @classmethod
    async def get_multi(cls, *, skip: int = 0, limit: int = 100):
        """Filter user list using skip and limit parameters."""
        query = UserModel.select().offset(skip).limit(limit)
        return await database.fetch_all(query=query)

    @classmethod
    async def get_by_email(cls, *, email: str):
        """Get user by email."""
        query = UserModel.select().where(email == UserModel.c.email)
        return await database.fetch_one(query=query)

    @classmethod
    async def create(cls, *, obj_in: UserCreate):
        """Create user by username, email and password."""
        hashed_password = get_password_hash(obj_in.password)
        user_in_db = UserInDB(**obj_in.dict(), hashed_password=hashed_password)
        query = UserModel.insert().values(**user_in_db.dict())
        return await database.execute(query=query)

    @classmethod
    async def update(
        cls,
        *,
        email: str,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ):
        """Update user."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        query = (
            UserModel
            .update()
            .where(email == UserModel.c.email)
            .values(**update_data)
        )
        return await database.execute(query=query)

    @classmethod
    async def remove(cls, *, email: str):
        """Delete user."""
        query = UserModel.delete().where(email == UserModel.c.email)
        return await database.execute(query=query)

    @staticmethod
    async def authenticate(
        *,
        email: str,
        password: str
    ):
        """Authenticate a user."""
        user = await CRUDUser.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
