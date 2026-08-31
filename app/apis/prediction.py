from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.databases import async_get_db
from app.schemas.ai_analysis import PneumoniaPredictionResponse
from app.services.prediction import (
    PredictionIntegrationService,
    PredictionModelUnavailableError,
    XrayFileNotFoundError,
    XrayNotFoundError,
)


router = APIRouter(
    prefix="/patients",
    tags=["ai-prediction"],
)


@router.post(
    "/{patient_id}/medical-records/{record_id}/prediction",
    response_model=PneumoniaPredictionResponse,
)
async def predict_pneumonia_api(
    patient_id: int,
    record_id: int,
    db: AsyncSession = Depends(async_get_db),
):
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

    except PredictionModelUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        )
      
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
