from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.models.user import User
from app.schemas.patient import PatientDetailResponse
from app.services.patient import PatientService


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@router.get(
    "/{patient_id}",
    response_model=PatientDetailResponse,
    status_code=status.HTTP_200_OK,
)
async def get_patient_detail(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-PTNT-003 환자 정보 상세 조회 API
    """

    service = PatientService(db)

    try:
        return await service.get_patient_detail(patient_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )