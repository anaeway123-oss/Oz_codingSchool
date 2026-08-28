from sqlalchemy.ext.asyncio import AsyncSession

from app.models.medical_record import MedicalRecord
from app.repositories.medical_record import MedicalRecordRepository
from app.repositories.patient import PatientRepository


class MedicalRecordService:
    def __init__(self, session: AsyncSession):
        self.patient_repository = PatientRepository(session)
        self.medical_record_repository = MedicalRecordRepository(session)

    async def get_medical_record_detail(
        self,
        patient_id: int,
        record_id: int,
    ) -> MedicalRecord:
        patient = await self.patient_repository.find_by_id(patient_id)

        if patient is None:
            raise ValueError("환자를 찾을 수 없습니다.")

        medical_record = (
            await self.medical_record_repository.find_by_patient_and_record_id(
                patient_id,
                record_id,
            )
        )

        if medical_record is None:
            raise ValueError("진료기록을 찾을 수 없습니다.")

        return medical_record