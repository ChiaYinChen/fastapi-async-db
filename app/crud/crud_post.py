"""CRUD for post."""
from typing import List, Optional

from ..models.article import Post as PostModel
from ..models.user import User as UserModel
from ..schemas.article import PostCreate


class CRUDPost:

    @classmethod
    async def get_multi(
        cls, *, db_obj: UserModel, skip: int = 0, limit: int = 100
    ) -> List[PostModel]:
        """Filter post list using skip and limit parameters."""
        return await (
            PostModel.objects.filter(author=db_obj.user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @classmethod
    async def get_by_post_id(
        cls, *, post_id: int, db_obj: UserModel
    ) -> Optional[PostModel]:
        """Get post by post id."""
        return await (
            PostModel.objects.filter(author=db_obj.user_id)
            .filter(id=post_id)
            .get_or_none()
        )

    @classmethod
    async def create(
        cls, *, db_obj: UserModel, obj_in: PostCreate
    ) -> PostModel:
        """Create a post by current_user."""
        return await PostModel.objects.create(
            **obj_in.dict(), author=db_obj
        )

    @classmethod
    async def update(
        cls, *, db_obj: PostModel, obj_in: PostCreate
    ) -> PostModel:
        """Update post."""
        return await db_obj.update(**obj_in.dict())

    @classmethod
    async def remove(
        cls, *, db_obj: PostModel
    ) -> PostModel:
        """Delete post."""
        await db_obj.delete()
        return db_obj
