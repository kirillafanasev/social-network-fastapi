import fastapi
from fastapi import Depends, Request, status
from fastapi.responses import RedirectResponse
from app.auth.base import get_current_user
from app.db.schemas import UserReturnSchema


router = fastapi.APIRouter(prefix='/logout')


@router.get('/')
async def logout_get(
        request: Request,
        current_user: UserReturnSchema = Depends(get_current_user)
):
    url_index = request.app.url_path_for('index')
    rr = RedirectResponse(url=url_index, status_code=status.HTTP_303_SEE_OTHER)
    rr.delete_cookie("session")
    return rr
