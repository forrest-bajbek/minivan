from fastapi import APIRouter, HTTPException, status

from app.auth.auth_handler import get_password_hash
from app.models.pydantic import UserCreatePayloadSchema
from app.models.tortoise import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_admin(payload: UserCreatePayloadSchema):
    existing_admin = await User.filter(is_admin=True).first().values()
    if existing_admin is not None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot create Admin account. One already exists.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    admin = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        email=payload.email,
        full_name=payload.full_name,
        category=payload.category,
        is_admin=True,
    )
    await admin.save()
    return {"message": f"Admin account created for user '{admin.username}'"}
