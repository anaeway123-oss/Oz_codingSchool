from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_admin
from app.core.db.databases import async_get_db
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_users(
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-USER-004 회원 목록 조회 API

    JWT 인증 및 Admin 권한을 확인한 뒤,
    DB에 등록된 사용자 전체 목록을 조회합니다.
    """

    result = await db.execute(
        select(User).order_by(User.id)
    )

    users = result.scalars().all()

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
