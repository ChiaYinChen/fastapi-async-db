"""Router for post."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..crud.crud_post import CRUDPost
from ..dependencies import get_current_active_user
from ..models.user import User as UserModel
from ..schemas.article import PostCreate

router = APIRouter()


@router.get("/")
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Get a user post list."""
    return await CRUDPost.get_multi(db_obj=current_user, skip=skip, limit=limit)  # noqa: E501


@router.post("/", status_code=201)
async def create_post(
    post_in: PostCreate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Create a post."""
    return await CRUDPost.create(db_obj=current_user, obj_in=post_in)


@router.patch("/{post_id}")
async def update_post(
    post_id: int,
    post_in: PostCreate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Update post."""
    db_post = await CRUDPost.get_by_post_id(post_id=post_id, db_obj=current_user)  # noqa: E501
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return await CRUDPost.update(db_obj=db_post, obj_in=post_in)


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Delete post."""
    db_post = await CRUDPost.get_by_post_id(post_id=post_id, db_obj=current_user)  # noqa: E501
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    removed_post = await CRUDPost.remove(db_obj=db_post)
    return JSONResponse(
        status_code=200,
        content={"message": f"Deleted post {removed_post.title}"}
    )
