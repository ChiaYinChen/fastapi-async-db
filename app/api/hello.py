"""Router for hello world."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def hello():
    return {"message": "Hello world!"}
