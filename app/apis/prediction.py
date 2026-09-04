from fastapi import APIRouter, Depends, HTTPException, status
from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.core.redis_client import (
    PredictionResultTimeoutError,
    PredictionWorkerError,
)

from app.models.enums import Role
from app.models.user import User
from app.schemas.ai_analysis import PneumoniaPredictionResponse
from app.services.prediction import (
    PredictionIntegrationService,
    XrayFileNotFoundError,
    XrayNotFoundError,
)


router = APIRouter(
    prefix="/patients",
    tags=["ai-prediction"],
)


def validate_prediction_permission(current_user: User) -> None:
    # 승인된 STAFF 또는 ADMIN만 AI 예측 기능 사용 가능
    if current_user.role not in {Role.STAFF, Role.ADMIN}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="승인된 의료팀, 개발팀, 연구팀 또는 관리자만 사용할 수 있습니다.",
        )


# 폐렴 AI 예측 실행
@router.post(
    "/{patient_id}/medical-records/{record_id}/ai-predictions",
    response_model=PneumoniaPredictionResponse,
    status_code=status.HTTP_200_OK,
)
async def predict_pneumonia_api(
    patient_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    validate_prediction_permission(current_user)

    service = PredictionIntegrationService(db)

    try:
        return await service.predict_medical_record(
            patient_id=patient_id,
            record_id=record_id,
        )

    except XrayNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except XrayFileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )

    except PredictionResultTimeoutError as error:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=str(error),
        )

    except (RedisError, PredictionWorkerError) as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


# 저장된 폐렴 AI 예측 결과 조회
@router.get(
    "/{patient_id}/medical-records/{record_id}/ai-predictions",
    response_model=list[PneumoniaPredictionResponse],
    status_code=status.HTTP_200_OK,
)
async def get_pneumonia_predictions(
    patient_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    validate_prediction_permission(current_user)

    service = PredictionIntegrationService(db)

    try:
        return await service.get_prediction_results(
            patient_id=patient_id,
            record_id=record_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
