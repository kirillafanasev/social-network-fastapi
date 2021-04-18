import fastapi
from fastapi import Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt
from app.config import settings
from app.db.crud import get_user_by_login, create_user
from app.db.schemas import UserReturnSchema
from app.models.base import RegisterForm


templates = Jinja2Templates(directory='templates')

router = fastapi.APIRouter(prefix='/register')


@router.get('/')
async def register_get(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/')
async def register_post(
        request: Request,
        user: RegisterForm = Depends(RegisterForm.as_form)
):

    database = request.app.state.db
    user_exist = await get_user_by_login(database, user.login)

    if user_exist:
        return templates.TemplateResponse(
            'user_exists.html',
            {
                'request': request,
                'user': user_exist,
            }
        )

    user_id = await create_user(database, user)

    current_user = UserReturnSchema(id=user_id, **user.dict())

    token = jwt.encode(
        {'current_user': current_user.dict()},
        settings.SECRET_KEY
    )
    url_home = request.app.url_path_for('home')
    rr = RedirectResponse(url=url_home, status_code=status.HTTP_303_SEE_OTHER)
    rr.set_cookie(
        "session",
        token,
        expires=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return rr
