"""Schema for Article."""
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    """Create input."""
    title: str = Field(..., max_length=200)
