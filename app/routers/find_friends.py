import fastapi
from fastapi import Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth.base import get_current_user
from app.db.crud import (
    get_potential_friends, write_friend, get_users_by_name_surname
)
from app.db.schemas import UserReturnSchema
from app.db.utils import prepare_users_to_form
from app.models.base import UserAddFriendForm, NameSurnameForm
from . import templates


router = fastapi.APIRouter(prefix='/friends')


@router.get('/find-friends', response_class=HTMLResponse)
async def find_friends(
        request: Request,
        current_user: UserReturnSchema = Depends(get_current_user)
):
    current_user_id = current_user.id

    database = request.app.state.db

    entries = await get_potential_friends(db=database, user_id=current_user_id)
    potential_friends = prepare_users_to_form(entries)

    return templates.TemplateResponse(
        'find-friends.html',
        {
            'request': request,
            'user': current_user,
            'potential_friends': potential_friends,
        }
    )


@router.post('/find-users-name-surname', response_class=HTMLResponse)
async def find_users_name_surname(
        request: Request,
        current_user: UserReturnSchema = Depends(get_current_user),
        name_surname: NameSurnameForm = Depends(NameSurnameForm.as_form)
):
    current_user_id = current_user.id
    database = request.app.state.db

    entries = await get_users_by_name_surname(
        user_id=current_user_id,
        db=database,
        name_surname=name_surname
    )

    potential_friends = prepare_users_to_form(entries)

    return templates.TemplateResponse(
        'find-friends.html',
        {
            'request': request,
            'user': current_user,
            'potential_friends': potential_friends,
        }
    )


@router.post('/add-friend', response_class=HTMLResponse)
async def add_friend(
        request: Request,
        current_user: UserReturnSchema = Depends(get_current_user),
        friend: UserAddFriendForm = Depends(UserAddFriendForm.as_form)
):
    database = request.app.state.db

    await write_friend(
        db=database,
        user_id=current_user.id,
        friend_id=friend.friend_id
    )

    find_friends_url = request.app.url_path_for('find_friends')
    rr = RedirectResponse(
        find_friends_url,
        status_code=status.HTTP_303_SEE_OTHER
    )
    return rr
