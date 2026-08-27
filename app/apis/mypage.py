from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ConfigDict

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.models.enums import Department, Gender, Role
from app.models.user import User
from app.schemas.user import UserProfileUpdate
from app.services.user import UserService


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
    current_user: User = Depends(get_current_user),
):
    """
    REQ-USER-006 마이페이지 조회 API

    JWT 인증을 통해 현재 로그인한 사용자의 정보를 조회합니다.
    """

    return current_user


@router.patch(
    "/me",
    response_model=MyPageResponse,
    status_code=status.HTTP_200_OK,
)
async def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-USER-007 회원 정보 수정 API

    로그인한 사용자의 부서와 휴대폰 번호를 부분 수정합니다.
    """

    service = UserService(db)

    try:
        return await service.update_profile(
            user=current_user,
            profile_data=profile_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
