from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient
from app.repositories.patient import PatientRepository


class PatientService:
    def __init__(self, session: AsyncSession):
        self.repository = PatientRepository(session)

    async def get_patient_detail(self, patient_id: int) -> Patient:
        patient = await self.repository.find_by_id(patient_id)

        if patient is None:
            raise ValueError("환자를 찾을 수 없습니다.")

        return patient