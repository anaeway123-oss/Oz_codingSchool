from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

# TODO: JWT 인증 모듈(공통) 완료 시 실제 get_current_user 의존성으로 대체/연결
def get_current_user(db: Session = Depends(get_db)) -> User:

    
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다."
        )
    return user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def withdraw_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    [REQ-USER-009] 로그인된 사용자 본인 계정을 탈퇴하고 Database에서 관련 정보를 즉시 삭제합니다.
    """
    # 1. 로그인 사용자 본인 계정 즉시 삭제
    db.delete(current_user)
    db.commit()
    
    return None