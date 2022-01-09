"""Schema for Token."""
from pydantic import BaseModel


class Token(BaseModel):
    """Output."""
    access_token: str
    token_type: str
