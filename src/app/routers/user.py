import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordRequestForm, SecurityScopes
from jose import JWTError
from pydantic import ValidationError

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_password_hash
from app.models.enums import ScopeEnum
from app.models.tortoise import User, UserSchema
from app.routers import crud

from app.models.pydantic import (  # isort:skip
    UserCreatePayloadSchema,
    UserPasswordResetPayloadSchema,
)

from app.auth.auth_handler import (  # isort:skip
    decodeJWT,
    encodeJWT,
    Token,
    TokenData,
    verify_password,
)

logger = logging.getLogger("uvicorn")

router = APIRouter(tags=["user"])


async def get_user(username: str) -> User:
    user_dict = await crud.get_user_from_username(username)
    if user_dict is None:
        return None
    return User(**user_dict)


async def authenticate_user(username: str, password: str) -> User:
    user = await get_user(username)
    if verify_password(password, user.password_hash):
        return user
    return None


async def validate_scopes(scopes: list[str | None]) -> list[str]:
    requested_scopes = set()
    if not scopes:
        requested_scopes.add(ScopeEnum.READ.value)
    for scope in scopes:
        if scope not in ScopeEnum.allowed_values():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid scope: '{scope}'",
                headers={"WWW-Authenticate": "Bearer"},
            )
        requested_scopes.add(scope)
        if scope == ScopeEnum.WRITE.value:
            requested_scopes.add(ScopeEnum.READ.value)
    return sorted(list(requested_scopes))


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(JWTBearer()),
) -> User:
    authenticate_value = (
        f"Bearer scope={security_scopes.scope_str}"
        if security_scopes.scopes
        else "Bearer"
    )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = decodeJWT(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(username=username, scopes=token_scopes)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: User = Security(get_current_user)):
    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_admin_user(
    current_active_user: User = Depends(get_current_active_user),
):
    if not current_active_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient permissions",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_active_user


@router.post("/token", response_model=Token)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = await authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Disabled User",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = await validate_scopes(form_data.scopes)
    access_token = encodeJWT(data={"sub": user.username, "scopes": scopes})
    token = Token(access_token=access_token, token_type="bearer")
    return token


@router.post(
    "/user/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_admin_user)],
)
async def create_user(payload: UserCreatePayloadSchema = Body(...)) -> Token:
    if await crud.user_exists(payload.username):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username already exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        email=payload.email,
        full_name=payload.full_name,
        category=payload.category,
    )
    await user.save(force_create=True)
    return {"message": f"Successfully created user '{user.username}'"}


@router.put(
    "/user/password/reset",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(get_current_active_admin_user)],
)
async def user_password_reset(payload: UserPasswordResetPayloadSchema):
    user_exists = await crud.user_exists(payload.username)
    if not user_exists:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User does not exist: '{payload.username}'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(payload.username)
    await user.select_for_update()
    user.password_hash = get_password_hash(payload.new_password)
    await user.save(update_fields=["password_hash"])
    return {"message": f"Password successfully reset for user '{user.username}'"}


@router.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: User = Security(get_current_user)):
    return current_user
