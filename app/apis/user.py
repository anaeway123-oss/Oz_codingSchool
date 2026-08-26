from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.databases import async_get_db
from app.schemas.user import UserCreate
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    db: AsyncSession = Depends(async_get_db),
):
    service = UserService(db)

    try:
        user = await service.create_user(user_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "department": user.department,
        "gender": user.gender,
        "phone_number": user.phone_number,
        "role": user.role,
        "is_active": user.is_active,
    }