import fastapi
from fastapi import Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt
from starlette.requests import Request
from app.auth.base import check_encrypted_password
from app.db.crud import get_user_by_login
from app.db.schemas import UserReturnSchema
from app.config import settings
from app.models.base import LoginForm


templates = Jinja2Templates(directory='templates')

router = fastapi.APIRouter(prefix='/login')


@router.get('/')
async def login_get(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/', response_class=HTMLResponse)
async def login_post(
        request: Request,
        user_login: LoginForm = Depends(LoginForm.as_form)
):
    database = request.app.state.db
    user = await get_user_by_login(database, user_login.login)

    if not user:
        return templates.TemplateResponse(
            'login_not_exist.html',
            {
                'request': request,
                'user': user_login.login
            }
        )

    user = dict(user)
    pwd_check = check_encrypted_password(
        user_login.password,
        user['password']
    )
    if pwd_check:
        current_user = UserReturnSchema(**user)
        token = jwt.encode(
            {'current_user': current_user.dict()},
            settings.SECRET_KEY
        )
        url_home = request.app.url_path_for('home')
        res = RedirectResponse(
            url=url_home,
            status_code=status.HTTP_303_SEE_OTHER
        )
        res.set_cookie(
            "session",
            token,
            expires=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    else:
        res = templates.TemplateResponse(
            'login_pwd_not_valid.html',
            {
                'request': request,
                'user': user
            }
        )
    return res
