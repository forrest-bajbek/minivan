from fastapi import APIRouter, Body

from app.auth.auth_handler import signJWT
from app.models.pydantic import UserAuthSchema, UserSchema

router = APIRouter()

users = []


@router.post("/user/signup")
def user_signup(user: UserSchema = Body(...)):
    users.append(user)  # replace with db call, hash password before storing
    return signJWT(user.email)


def check_user(data: UserAuthSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@router.post("/user/auth")
def user_auth(user: UserAuthSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {"error": "Invalid authentication credentials."}
