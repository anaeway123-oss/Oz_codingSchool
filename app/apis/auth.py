from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.databases import async_get_db
from app.core.security import create_access_token, decode_refresh_token
from app.schemas.user import UserLogin
from app.services.user import UserService


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
    login_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(async_get_db),
):
    service = UserService(db)

    try:
        tokens = await service.login(login_data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        )

    # Refresh Token은 JavaScript에서 접근할 수 없도록
    # httpOnly 쿠키로 전달
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
    )

    # Access Token만 응답 Body에 반환
    return {
        "access_token": tokens["access_token"],
        "token_type": tokens["token_type"],
    }


@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str | None = Cookie(default=None),
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token이 없습니다.",
        )

    try:
        user_id = decode_refresh_token(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 Refresh Token입니다.",
        )

    new_access_token = create_access_token(user_id)

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        samesite="lax",
    )

    return {
        "message": "로그아웃 되었습니다."
    }