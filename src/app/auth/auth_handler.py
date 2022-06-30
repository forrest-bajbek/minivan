import time
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config import get_settings

settings = get_settings()
JWT_SECRET = settings.jwt_secret
JWT_ALGORITHM = settings.jwt_algorithm


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def encodeJWT(data: dict) -> str:
    to_encode = data.copy()
    expire = time.time() + timedelta(minutes=settings.jwt_expire_minutes).seconds
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
