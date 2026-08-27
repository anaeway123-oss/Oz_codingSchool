from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from app.core.auth import get_current_user
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
    current_user: User = Depends(get_current_user),
):
    """
    REQ-USER-006 마이페이지 조회 API

    JWT 인증을 통해 현재 로그인한 사용자의 정보를 조회합니다.
    """

    return current_user
