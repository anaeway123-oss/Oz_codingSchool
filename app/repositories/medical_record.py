from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.models.xray_image import XrayImage


class MedicalRecordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 환자 ID로 환자 조회
    async def find_patient_by_id(
        self,
        patient_id: int,
    ) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.id == patient_id)
        )
        return result.scalar_one_or_none()

    # 진료 차트 번호 중복 확인
    async def find_by_chart_number(
        self,
        chart_number: str,
    ) -> MedicalRecord | None:
        result = await self.session.execute(
            select(MedicalRecord).where(
                MedicalRecord.chart_number == chart_number
            )
        )
        return result.scalar_one_or_none()

    # 진료기록을 세션에 추가
    def add_medical_record(
        self,
        medical_record: MedicalRecord,
    ) -> None:
        self.session.add(medical_record)

    # X-Ray 이미지 정보를 세션에 추가
    def add_xray_image(
        self,
        xray_image: XrayImage,
    ) -> None:
        self.session.add(xray_image)

    # DB에 반영하여 생성된 ID 확보
    async def flush(self) -> None:
        await self.session.flush()

    # 전체 작업 확정
    async def commit(self) -> None:
        await self.session.commit()

    # 오류 발생 시 전체 작업 취소
    async def rollback(self) -> None:
        await self.session.rollback()

    # 저장 후 응답에 필요한 컬럼과 X-Ray 관계를 함께 조회
    async def refresh_medical_record(
        self,
        medical_record: MedicalRecord,
    ) -> MedicalRecord:
        result = await self.session.execute(
            select(MedicalRecord)
            .options(selectinload(MedicalRecord.xray_images))
            .where(MedicalRecord.id == medical_record.id)
        )

        return result.scalar_one()

    # 환자 ID로 진료기록 목록 조회
    async def find_all_by_patient_id(
        self,
        patient_id: int,
    ) -> list[MedicalRecord]:
        result = await self.session.execute(
            select(MedicalRecord)
            .where(MedicalRecord.patient_id == patient_id)
            .order_by(MedicalRecord.id)
        )

        return list(result.scalars().all())

    # 환자 ID와 진료기록 ID로 상세 조회
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