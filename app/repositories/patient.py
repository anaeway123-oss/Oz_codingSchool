from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient


class PatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, patient_id: int) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.id == patient_id)
        )

        return result.scalar_one_or_none()