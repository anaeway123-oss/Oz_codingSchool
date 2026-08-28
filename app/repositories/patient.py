from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import Gender
from app.models.medical_record import MedicalRecord
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

    # 환자와 연결된 진료기록 및 X-Ray 조회
    async def find_by_id_with_records(
        self,
        patient_id: int,
    ) -> Patient | None:
        result = await self.session.execute(
            select(Patient)
            .options(
                selectinload(Patient.medical_records).selectinload(
                    MedicalRecord.xray_images
                )
            )
            .where(Patient.id == patient_id)
        )

        return result.scalar_one_or_none()

    # 환자 삭제
    async def delete(self, patient: Patient) -> None:
        await self.session.delete(patient)

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

    # 환자 목록 조회 + 이름/성별/나이 범위 필터
    async def find_all(
        self,
        name: str | None = None,
        gender: Gender | None = None,
        min_age: int | None = None,
        max_age: int | None = None,
    ) -> list[Patient]:
        query = select(Patient)

        if name:
            query = query.where(Patient.name.ilike(f"%{name}%"))

        if gender is not None:
            query = query.where(Patient.gender == gender)

        if min_age is not None:
            query = query.where(Patient.age >= min_age)

        if max_age is not None:
            query = query.where(Patient.age <= max_age)

        query = query.order_by(Patient.id)

        result = await self.session.execute(query)

        return list(result.scalars().all())
