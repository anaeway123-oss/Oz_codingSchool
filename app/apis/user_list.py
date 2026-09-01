from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_admin
from app.core.db.databases import async_get_db
from app.models.enums import Department
from app.models.user import User
from app.schemas.user import UserRoleUpdate
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_users(
    query: str | None = Query(default=None),
    department: Department | None = Query(default=None),
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-USER-004 회원 목록 조회 API

    JWT 인증 및 Admin 권한을 확인한 뒤,
    DB에 등록된 사용자 전체 목록을 조회합니다.
    """

    statement = select(User)

    # 이름 또는 이메일 부분 검색
    if query:
        keyword = f"%{query.strip()}%"
        statement = statement.where(
            or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            )
        )

    # 부서 필터
    if department is not None:
        statement = statement.where(User.department == department)

    result = await db.execute(
        statement.order_by(User.id)
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
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]

@router.patch(
    "/{user_id}/role",
    status_code=status.HTTP_200_OK,
)
async def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    current_admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-USER-005 회원 권한 변경 API

    Admin 권한의 사용자가 선택한 회원의 권한을 변경합니다.
    """

    service = UserService(db)

    try:
        user = await service.update_role(
            user_id=user_id,
            role_data=role_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
    }
