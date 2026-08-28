from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.db.databases import async_get_db
from app.models.enums import Department, Role
from app.models.user import User
from app.schemas.medical_record import (
    MedicalRecordCreateResponse,
    MedicalRecordDetailResponse,
)
from app.services.medical_record import (
    DuplicateChartNumberError,
    MedicalRecordService,
    PatientNotFoundError,
)


router = APIRouter(
    prefix="/patients",
    tags=["medical-records"],
)


# 진료기록 등록 + X-Ray 이미지 업로드
@router.post(
    "/{patient_id}/medical-records",
    response_model=MedicalRecordCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_medical_record(
    patient_id: int,
    chart_number: str = Form(...),
    symptoms: str = Form(...),
    xray_image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):
    # 진료기록 등록은 승인된 의료 실무진만 가능
    if (
        current_user.role != Role.STAFF
        or current_user.department != Department.MEDICAL
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="의료 실무진만 진료기록을 등록할 수 있습니다.",
        )

    # 업로드 파일의 Content-Type 확인
    if xray_image.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Ray 이미지는 JPG, JPEG, PNG 형식만 업로드할 수 있습니다.",
        )

    service = MedicalRecordService(db)

    try:
        medical_record = await service.create_medical_record(
            patient_id=patient_id,
            chart_number=chart_number,
            symptoms=symptoms,
            xray_image=xray_image,
            uploader_id=current_user.id,
        )
    except PatientNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
    except DuplicateChartNumberError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )

    return medical_record


# 진료기록 상세 조회
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
