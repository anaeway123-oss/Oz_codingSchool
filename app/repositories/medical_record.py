from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.medical_record import MedicalRecord


class MedicalRecordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_patient_and_record_id(
        self,
        patient_id: int,
        record_id: int,
    ) -> MedicalRecord | None:
        result = await self.session.execute(
            select(MedicalRecord)
            .options(selectinload(MedicalRecord.xray_images))
            .where(
                MedicalRecord.id == record_id,
                MedicalRecord.patient_id == patient_id,
            )
        )

        return result.scalar_one_or_none()