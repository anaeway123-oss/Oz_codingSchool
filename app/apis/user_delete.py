from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def withdraw_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-USER-009 회원 탈퇴 API

    JWT 인증을 통해 현재 로그인한 사용자 본인의 계정을 삭제합니다.
    """

    await db.delete(current_user)
    await db.commit()

    return None
