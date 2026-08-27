from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.databases import async_get_db
from app.models.enums import Department, Gender, Role
from app.models.user import User


# 마이페이지 조회 응답 형식
class MyPageResponse(BaseModel):
    name: str | None
    email: str | None
    department: Department
    gender: Gender
    phone_number: str | None
    role: Role

    model_config = ConfigDict(from_attributes=True)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    response_model=MyPageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_page(
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-USER-006 마이페이지 조회 API

    현재 단계에서는 인증/JWT를 적용하지 않고,
    DB에 등록된 활성 사용자 1명을 조회합니다.
    """

    result = await db.execute(
        select(User)
        .where(User.is_active.is_(True))
        .order_by(User.id)
        .limit(1)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="조회할 사용자가 없습니다.",
        )

    return user


