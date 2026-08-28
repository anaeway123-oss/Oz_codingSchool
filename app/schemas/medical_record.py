from datetime import datetime

from pydantic import BaseModel, ConfigDict


class XrayImageResponse(BaseModel):
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordDetailResponse(BaseModel):
    id: int
    chart_number: str
    symptoms: str
    xray_images: list[XrayImageResponse]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)