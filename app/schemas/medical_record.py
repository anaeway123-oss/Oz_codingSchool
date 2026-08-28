from datetime import datetime

from pydantic import BaseModel, ConfigDict


# X-Ray 이미지 응답 데이터
class XrayImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    shooting_datetime: datetime


# 진료기록 등록 응답 데이터
class MedicalRecordCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    chart_number: str
    symptoms: str
    created_at: datetime
    xray_images: list[XrayImageResponse]
