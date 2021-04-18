import fastapi
from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from app.auth.base import get_current_user
from app.db.crud import get_existing_friends, get_user_by_id
from app.db.schemas import UserReturnSchema
from app.db.utils import prepare_users_to_form


templates = Jinja2Templates(directory='templates')

router = fastapi.APIRouter()


@router.get('/')
async def index(
        request: Request,
):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/home')
async def home(
        request: Request,
        current_user: UserReturnSchema = Depends(get_current_user)
):

    database = request.app.state.db

    user = await get_user_by_id(database, current_user.id)
    friends_db = await get_existing_friends(database, current_user.id)
    friends = prepare_users_to_form(friends_db)

    return templates.TemplateResponse(
        'home.html',
        {
            'request': request,
            'user': user,
            'friends': friends,
        }
    )
