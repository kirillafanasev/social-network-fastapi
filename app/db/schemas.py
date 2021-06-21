from typing import Optional
from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    login: str
    name: str
    surname: str
    age: Optional[int] = None
    gender: str
    hobbies: str
    city: str


class UserReturnSchema(UserBaseSchema):
    id: int


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchema(UserCreateSchema):
    id: int

    class Config:
        orm_mode = True
