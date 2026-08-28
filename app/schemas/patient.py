from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import Gender


# 환자 정보 등록 요청 데이터
class PatientCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=30)
    age: int = Field(ge=0, le=150)
    gender: Gender
    phone: str = Field(
        min_length=10,
        max_length=11,
        pattern=r"^01[016789]\d{7,8}$",
    )


# 환자 정보 수정 요청 데이터
class PatientUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=30)
    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=11,
        pattern=r"^01[016789]\d{7,8}$",
    )


# 환자 정보 응답 데이터
class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    gender: Gender | None
    phone: str
    created_at: datetime
    updated_at: datetime | None


# 환자 정보 상세 조회 응답 데이터
class PatientDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    gender: Gender | None
    phone: str
    age: int
