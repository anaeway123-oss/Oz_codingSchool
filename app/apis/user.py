from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_admin, get_current_user
from app.core.db.databases import async_get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserPasswordUpdate
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# 회원가입
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


# 관리자 회원 목록 조회
@router.get("")
async def get_users(
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(async_get_db),
):
    repository = UserRepository(db)
    users = await repository.get_all_users()

    return [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "department": user.department,
            "gender": user.gender,
            "phone_number": user.phone_number,
            "is_active": user.is_active,
        }
        for user in users
    ]


# 비밀번호 변경
@router.patch("/me/password")
async def change_password(
    password_data: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    service = UserService(db)

    try:
        await service.change_password(
            current_user,
            password_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    return {
        "message": "비밀번호가 변경되었습니다."
    }