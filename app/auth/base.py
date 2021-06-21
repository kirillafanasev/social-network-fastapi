from fastapi import Depends
from fastapi.security import APIKeyCookie
from jose import jwt
from passlib.context import CryptContext
from app.db.schemas import UserReturnSchema
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password):
    return pwd_context.hash(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


cookie_sec = APIKeyCookie(name="session")


def get_current_user(session: str = Depends(cookie_sec)) -> UserReturnSchema:
    payload = jwt.decode(session, settings.SECRET_KEY)
    current_user = payload.get('current_user')
    return UserReturnSchema(**current_user)
