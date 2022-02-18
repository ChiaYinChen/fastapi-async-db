"""Router for logout."""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/logout")
async def logout():
    """Logout and remove cookie."""
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
