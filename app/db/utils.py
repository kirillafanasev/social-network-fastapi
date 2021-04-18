from aiomysql.sa.result import Mapping
from typing import List
from .schemas import UserReturnSchema


def prepare_user_to_form(user: Mapping) -> UserReturnSchema:
    user_dict = dict(user)
    del user_dict['password']
    return UserReturnSchema(**user_dict)


def prepare_users_to_form(users: List[Mapping]) -> List[UserReturnSchema]:
    res = list(map(prepare_user_to_form, users))
    return res
