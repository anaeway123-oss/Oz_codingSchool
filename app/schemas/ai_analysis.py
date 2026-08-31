from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PneumoniaPredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    record_id: int
    is_pneumonia: bool
    confidence: float = Field(ge=0.0, le=1.0)
    heatmap_url: str | None = None
    ai_model: str
    created_at: datetime
