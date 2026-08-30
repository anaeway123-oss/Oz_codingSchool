from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.medical_record import MedicalRecord
from app.models.xray_image import XrayImage
from app.repositories.medical_record import MedicalRecordRepository
from app.repositories.patient import PatientRepository


# 프로젝트의 X-Ray 이미지 저장 위치
BASE_DIR = Path(__file__).resolve().parent.parent.parent
XRAY_DIR = BASE_DIR / "media" / "xrays"

# 허용할 X-Ray 이미지 확장자
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class PatientNotFoundError(ValueError):
    pass


class DuplicateChartNumberError(ValueError):
    pass


class MedicalRecordService:
    def __init__(self, session: AsyncSession):
        self.repository = MedicalRecordRepository(session)
        self.patient_repository = PatientRepository(session)

    # 업로드된 X-Ray 파일 형식 확인
    @staticmethod
    def validate_xray_file(xray_image: UploadFile) -> str:
        if not xray_image.filename:
            raise ValueError("X-Ray 이미지 파일명이 없습니다.")

        extension = Path(xray_image.filename).suffix.lower()

        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(
                "X-Ray 이미지는 JPG, JPEG, PNG 형식만 업로드할 수 있습니다."
            )

        return extension

    # X-Ray 이미지를 로컬 저장소에 저장
    @staticmethod
    async def save_xray_file(
        xray_image: UploadFile,
        extension: str,
    ) -> tuple[Path, str]:
        from uuid import uuid4

        XRAY_DIR.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid4().hex}{extension}"
        file_path = XRAY_DIR / filename

        contents = await xray_image.read()

        if not contents:
            raise ValueError("빈 X-Ray 이미지 파일은 업로드할 수 없습니다.")

        try:
            file_path.write_bytes(contents)
        except OSError as error:
            raise RuntimeError("X-Ray 이미지 저장에 실패했습니다.") from error

        image_url = f"/media/xrays/{filename}"

        return file_path, image_url

    # 진료기록과 X-Ray 이미지 등록
    async def create_medical_record(
        self,
        patient_id: int,
        chart_number: str,
        symptoms: str,
        xray_image: UploadFile,
        uploader_id: int,
    ) -> MedicalRecord:
        # 환자 존재 여부 확인
        patient = await self.repository.find_patient_by_id(patient_id)

        if patient is None:
            raise PatientNotFoundError("존재하지 않는 환자입니다.")

        # 필수 입력값 확인
        if not chart_number.strip():
            raise ValueError("진료 차트 넘버를 입력해주세요.")

        if not symptoms.strip():
            raise ValueError("진료된 증상을 입력해주세요.")

        # 진료 차트 번호 중복 확인
        duplicate_record = await self.repository.find_by_chart_number(
            chart_number
        )

        if duplicate_record is not None:
            raise DuplicateChartNumberError(
                "이미 사용 중인 진료 차트 넘버입니다."
            )

        # X-Ray 파일 형식 확인
        extension = self.validate_xray_file(xray_image)

        saved_file_path: Path | None = None

        try:
            # 진료기록 생성
            medical_record = MedicalRecord(
                patient_id=patient_id,
                chart_number=chart_number.strip(),
                symptoms=symptoms.strip(),
            )
            self.repository.add_medical_record(medical_record)

            # X-Ray 연결에 필요한 진료기록 ID 확보
            await self.repository.flush()

            # X-Ray 파일을 로컬 저장소에 저장
            saved_file_path, image_url = await self.save_xray_file(
                xray_image=xray_image,
                extension=extension,
            )

            # X-Ray DB 정보 생성
            xray = XrayImage(
                record_id=medical_record.id,
                uploader_id=uploader_id,
                image_url=image_url,
                shooting_datetime=datetime.now(),
            )
            self.repository.add_xray_image(xray)

            # 진료기록과 X-Ray 정보를 한 번에 확정
            await self.repository.commit()

            return await self.repository.refresh_medical_record(
                medical_record
            )

        except Exception:
            await self.repository.rollback()

            # DB 저장이 실패하면 이미 저장된 로컬 파일도 제거
            if saved_file_path is not None and saved_file_path.exists():
                saved_file_path.unlink()

            raise

    # 진료기록 목록 조회
    async def get_medical_records(
        self,
        patient_id: int,
    ) -> list[MedicalRecord]:
        # 환자 존재 여부 확인
        patient = await self.patient_repository.find_by_id(patient_id)

        if patient is None:
            raise PatientNotFoundError("존재하지 않는 환자입니다.")

        # 해당 환자의 진료기록만 조회
        return await self.repository.find_all_by_patient_id(
            patient_id
        )

    # 진료기록 상세 조회
    async def get_medical_record_detail(
        self,
        patient_id: int,
        record_id: int,
    ) -> MedicalRecord:
        patient = await self.patient_repository.find_by_id(patient_id)

        if patient is None:
            raise ValueError("환자를 찾을 수 없습니다.")

        medical_record = await self.repository.find_by_patient_and_record_id(
            patient_id,
            record_id,
        )

        if medical_record is None:
            raise ValueError("진료기록을 찾을 수 없습니다.")

        return medical_record