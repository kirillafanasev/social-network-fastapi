from typing import List
import fastapi
from fastapi import Request, Depends
from app.auth.base import get_current_user
from app.db.crud import get_users_by_name_surname
from app.db.schemas import UserReturnSchema
from app.models.base import NameSurnameForm


router = fastapi.APIRouter(prefix='/api/v1')


@router.post('/find-users-name-surname', response_model=List[UserReturnSchema])
async def find_users_name_surname(
        request: Request,
        name_surname: NameSurnameForm,
        current_user: UserReturnSchema = Depends(get_current_user),
):
    current_user_id = current_user.id
    database = request.app.state.db

    entries = await get_users_by_name_surname(
        user_id=current_user_id,
        db=database,
        name_surname=name_surname
    )

    return entries
