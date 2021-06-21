from aiomysql.sa.result import Mapping
from itertools import chain
from sqlalchemy.sql import select
from typing import List
from databases import Database
from app.auth.base import encrypt_password
from app.models.base import RegisterForm
from .models import user_table, user_friend


async def get_user_by_login(db: Database, login: str):
    query = user_table.select().where(user_table.c.login == login)
    return await db.fetch_one(query)


async def get_user_by_id(db: Database, user_id: int):
    query = user_table.select().where(user_table.c.id == user_id)
    return await db.fetch_one(query)


async def get_existing_friends_ids(
        db: Database,
        user_id: int
) -> List[Mapping]:
    query = select(
        [user_friend.c.friend_id]).where(user_friend.c.user_id == user_id)
    return await db.fetch_all(query)


async def get_existing_friends(
        db: Database,
        user_id: int
) -> List[Mapping]:
    existing_friends = await get_existing_friends_ids(db, user_id)
    existing_friends_ids = [f[0] for f in existing_friends]

    query = user_table.select().where(user_table.c.id.in_(existing_friends_ids))
    return await db.fetch_all(query)


async def get_potential_friends(
        db: Database,
        user_id: int
) -> List[Mapping]:

    existing_friends = await get_existing_friends_ids(db, user_id)
    existing_friends_ids = [f[0] for f in existing_friends]
    exclude_user_ids = list(
        chain.from_iterable(
            [existing_friends_ids, [user_id]]
        )
    )
    query = user_table.select().where(user_table.c.id.notin_(exclude_user_ids))
    return await db.fetch_all(query)


async def write_friend(db: Database, user_id: int, friend_id: int):

    query = user_friend.insert().values(user_id=user_id, friend_id=friend_id)
    await db.execute(query)
    query = user_friend.insert().values(user_id=friend_id, friend_id=user_id)
    await db.execute(query)


async def create_user(db: Database, user: RegisterForm):
    pwd = encrypt_password(user.password)
    query = user_table.insert().values(
        login=user.login,
        password=pwd,
        name=user.name,
        surname=user.surname,
        age=user.age,
        gender=user.gender,
        hobbies=user.hobbies,
        city=user.city
    )
    user_id = await db.execute(query)
    return user_id
