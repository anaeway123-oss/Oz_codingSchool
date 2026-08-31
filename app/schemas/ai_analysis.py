from typing import Literal

from pydantic import BaseModel, Field


class PneumoniaPredictionResponse(BaseModel):
    class_id: int = Field(ge=0, le=1)
    label: Literal["NORMAL", "PNEUMONIA"]
    is_pneumonia: bool
    confidence: float = Field(ge=0.0, le=1.0)
    normal_probability: float = Field(ge=0.0, le=1.0)
    pneumonia_probability: float = Field(ge=0.0, le=1.0)
