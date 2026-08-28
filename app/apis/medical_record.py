from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.models.user import User
from app.schemas.medical_record import MedicalRecordDetailResponse
from app.services.medical_record import MedicalRecordService


router = APIRouter(
    prefix="/patients",
    tags=["medical-records"],
)


@router.get(
    "/{patient_id}/medical-records/{record_id}",
    response_model=MedicalRecordDetailResponse,
    status_code=status.HTTP_200_OK,
)
async def get_medical_record_detail(
    patient_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    """
    REQ-MDR-003 진료기록 상세 조회 API
    """

    service = MedicalRecordService(db)

    try:
        return await service.get_medical_record_detail(
            patient_id=patient_id,
            record_id=record_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )