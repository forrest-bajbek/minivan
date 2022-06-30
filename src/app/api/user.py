from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from app.api import crud
from app.auth.auth_bearer import oauth2_scheme
from app.auth.auth_handler import decodeJWT, encodeJWT, verify_password, Token
from app.models.pydantic import UserSignupPayloadSchema
from app.models.tortoise import User, UserSchema

router = APIRouter()


async def authenticate_user(username: str, password: str):
    user = await crud.get_user_from_username(username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodeJWT(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_from_username(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/user/signup", response_model=Token)
async def create_user(payload: UserSignupPayloadSchema = Body(...)) -> Token:
    user = await crud.create_user(payload)
    if not user:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username already exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {"sub": user.username}
    access_token = encodeJWT(data)
    token = Token(access_token=access_token, token_type="bearer")
    return token


@router.post("/user/login", response_model=Token)
async def create_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encodeJWT(data={"sub": user.username})
    token = Token(access_token=access_token, token_type="bearer")
    return token


@router.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    return current_user
