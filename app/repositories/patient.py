from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient


class PatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 환자 ID로 조회
    async def find_by_id(self, patient_id: int) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.id == patient_id)
        )

        return result.scalar_one_or_none()

    # 새로운 환자 저장
    async def create(self, patient: Patient) -> Patient:
        self.session.add(patient)
        await self.session.commit()
        await self.session.refresh(patient)

        return patient

    # 환자 정보 수정
    async def update(
        self,
        patient: Patient,
        name: str | None = None,
        phone: str | None = None,
    ) -> Patient:
        if name is not None:
            patient.name = name

        if phone is not None:
            patient.phone = phone

        await self.session.commit()
        await self.session.refresh(patient)

        return patient
