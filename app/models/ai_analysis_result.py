from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, DECIMAL, ForeignKey, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.databases import Base


class AiAnalysisResult(Base):
    __tablename__ = "ai_analysis_results"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    record_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("medical_records.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_pneumonia: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidence: Mapped[Decimal] = mapped_column(DECIMAL(5, 2), nullable=False)
    heatmap_url: Mapped[str] = mapped_column(String(255), nullable=False)
    ai_model: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    medical_record: Mapped["MedicalRecord"] = relationship(
        back_populates="ai_analysis_results"
    )
