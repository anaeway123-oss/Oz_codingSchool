from pydantic import BaseModel, ConfigDict

from app.models.enums import Gender


class PatientDetailResponse(BaseModel):
    name: str
    gender: Gender | None
    phone: str
    age: int

    model_config = ConfigDict(from_attributes=True)