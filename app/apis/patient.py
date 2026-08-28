from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.models.user import User
from app.schemas.patient import (
    PatientCreate,
    PatientDetailResponse,
    PatientResponse,
    PatientUpdate,
)
from app.services.patient import PatientService


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


# 환자 정보 등록
@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_patient(
    patient_data: PatientCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    service = PatientService(db)

    try:
        return await service.create_patient(
            patient_data=patient_data,
            current_user=current_user,
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )


# 환자 정보 수정
@router.patch(
    "/{patient_id}",
    response_model=PatientResponse,
)
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    service = PatientService(db)

    try:
        return await service.update_patient(
            patient_id=patient_id,
            patient_data=patient_data,
            current_user=current_user,
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        )
    except LookupError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# 환자 정보 상세 조회
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
