"""Router for user."""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..crud.crud_user import CRUDUser
from ..dependencies import (
    get_current_active_superuser,
    get_current_active_user
)
from ..models.user import User as UserModel
from ..schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/me", response_model=User)
async def get_user_me(
    current_user: UserModel = Depends(get_current_active_user)
) -> Any:
    """Get the current logged in user."""
    return current_user


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_superuser),
) -> Any:
    """Get user list."""
    users = CRUDUser.get_multi(skip=skip, limit=limit)
    return await users


@router.get("/{email}", response_model=User)
async def get_user(
    email: str,
) -> Any:
    """Get user detail information."""
    db_user = await CRUDUser.get_by_email(email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=User, status_code=201)
async def create_user(
    user_in: UserCreate,
) -> Any:
    """Create a user."""
    db_user = await CRUDUser.get_by_email(email=user_in.email)
    if db_user:
        return JSONResponse(
            status_code=400,
            content={"message": "User already exist"}
        )
    return await CRUDUser.create(obj_in=user_in)


@router.patch("/{email}", response_model=User)
async def update_user(
    email: str,
    user_in: UserUpdate,
) -> Any:
    """Update user."""
    db_user = await CRUDUser.get_by_email(email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await CRUDUser.update(db_obj=db_user, obj_in=user_in)


@router.delete("/{email}")
async def delete_user(
    email: str,
) -> Any:
    """Delete user."""
    db_user = await CRUDUser.get_by_email(email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    removed_user = await CRUDUser.remove(db_obj=db_user)
    return JSONResponse(
        status_code=200,
        content={"message": f"Deleted user {removed_user.email}"}
    )
