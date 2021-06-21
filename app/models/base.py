from fastapi import Form
from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    login: str
    password: str


class RegisterForm(BaseModel):
    login: str
    password: str
    name: Optional[str] = ''
    surname: Optional[str] = ''
    age: Optional[int] = None
    gender: Optional[str] = ''
    hobbies: Optional[str] = ''
    city: Optional[str] = ''

    @classmethod
    def as_form(
        cls,
        login: str = Form(...),
        password: str = Form(...),
        name: Optional[str] = Form(''),
        surname: Optional[str] = Form(''),
        age: Optional[int] = Form(None),
        gender: Optional[str] = Form(''),
        hobbies: Optional[str] = Form(''),
        city: Optional[str] = Form('')
    ):
        return cls(
            login=login,
            password=password,
            name=name,
            surname=surname,
            age=age,
            gender=gender,
            hobbies=hobbies,
            city=city
        )


class LoginForm(BaseModel):
    login: str
    password: str

    @classmethod
    def as_form(
        cls,
        login: str = Form(...),
        password: str = Form(...)
    ):
        return cls(
            login=login,
            password=password
        )


class UserAddFriendForm(BaseModel):
    friend_id: int

    @classmethod
    def as_form(
        cls,
        friend_id: int = Form(...)
    ):
        return cls(
            friend_id=friend_id
        )
