"""CRUD for user."""
from typing import Any, Dict, List, Optional, Union

from ..core.security import get_password_hash, verify_password
from ..models.user import User as UserModel
from ..schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser:

    @classmethod
    async def get_multi(
        cls, *, skip: int = 0, limit: int = 100
    ) -> List[UserModel]:
        """Filter user list using skip and limit parameters."""
        return await UserModel.objects.offset(skip).limit(limit).all()

    @classmethod
    async def get_by_email(
        cls, *, email: str
    ) -> Optional[UserModel]:
        """Get user by email."""
        return await UserModel.objects.filter(email=email).get_or_none()

    @classmethod
    async def create(
        cls, *, obj_in: UserCreate
    ) -> UserModel:
        """Create user by username, email and password."""
        hashed_password = get_password_hash(obj_in.password)
        user_in_db = UserInDB(**obj_in.dict(), hashed_password=hashed_password)
        db_obj = UserModel(**user_in_db.dict())
        return await db_obj.save()

    @classmethod
    async def update(
        cls,
        *,
        db_obj: UserModel,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserModel:
        """Update user."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await db_obj.update(**update_data)

    @classmethod
    async def remove(
        cls, *, db_obj: UserModel
    ) -> UserModel:
        """Delete user."""
        await db_obj.delete()
        return db_obj

    @staticmethod
    async def authenticate(
        *,
        email: str,
        password: str
    ) -> Optional[UserModel]:
        """Authenticate a user."""
        user = await CRUDUser.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: UserModel) -> bool:
        """Check if user is active."""
        return user.is_active

    @staticmethod
    def is_superuser(user: UserModel) -> bool:
        """Check if user is superuser."""
        return user.is_superuser
