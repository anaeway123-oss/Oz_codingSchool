from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Department, Gender, Role
from app.models.patient import Patient
from app.models.user import User
from app.repositories.patient import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


# 프로젝트의 X-Ray 이미지 저장 위치
BASE_DIR = Path(__file__).resolve().parent.parent.parent
XRAY_DIR = BASE_DIR / "media" / "xrays"


class PatientService:
    def __init__(self, session: AsyncSession):
        self.repository = PatientRepository(session)

    # 환자 등록
    async def create_patient(
        self,
        patient_data: PatientCreate,
        current_user: User,
    ) -> Patient:
        has_allowed_role = current_user.role in {Role.STAFF, Role.ADMIN}
        is_medical_department = (
            current_user.department == Department.MEDICAL
        )

        if not (has_allowed_role and is_medical_department):
            raise PermissionError("환자 등록 권한이 없습니다.")

        new_patient = Patient(
            name=patient_data.name,
            age=patient_data.age,
            gender=patient_data.gender,
            phone=patient_data.phone,
        )

        return await self.repository.create(new_patient)

    # 환자 정보 수정
    async def update_patient(
        self,
        patient_id: int,
        patient_data: PatientUpdate,
        current_user: User,
    ) -> Patient:
        if current_user.role not in {Role.STAFF, Role.ADMIN}:
            raise PermissionError("환자 정보 수정 권한이 없습니다.")

        patient = await self.repository.find_by_id(patient_id)

        if patient is None:
            raise LookupError("환자를 찾을 수 없습니다.")

        update_data = patient_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            raise ValueError("수정할 정보를 하나 이상 입력해주세요.")

        return await self.repository.update(
            patient=patient,
            name=update_data.get("name"),
            phone=update_data.get("phone"),
        )

    # 환자 정보 상세 조회
    async def get_patient_detail(self, patient_id: int) -> Patient:
        patient = await self.repository.find_by_id(patient_id)

        if patient is None:
            raise ValueError("환자를 찾을 수 없습니다.")

        return patient

    # 환자 삭제
    async def delete_patient(
        self,
        patient_id: int,
        current_user: User,
    ) -> None:
        has_allowed_role = current_user.role in {Role.STAFF, Role.ADMIN}
        has_allowed_department = current_user.department in {
            Department.DEV,
            Department.MEDICAL,
            Department.RESEARCH,
        }

        if not (has_allowed_role and has_allowed_department):
            raise PermissionError("환자 삭제 권한이 없습니다.")

        # 진료기록 및 X-Ray까지 함께 조회
        patient = await self.repository.find_by_id_with_records(patient_id)

        if patient is None:
            raise LookupError("환자를 찾을 수 없습니다.")

        # 삭제할 X-Ray 파일 경로를 먼저 확보
        xray_file_paths: list[Path] = []

        for medical_record in patient.medical_records:
            for xray_image in medical_record.xray_images:
                if xray_image.image_url.startswith("/media/"):
                    relative_path = xray_image.image_url.removeprefix("/media/")
                    file_path = BASE_DIR / "media" / relative_path
                    xray_file_paths.append(file_path)

        try:
            # DB에서 환자 삭제 대상으로 지정
            await self.repository.delete(patient)

            # DB 삭제 확정
            await self.repository.session.commit()

        except Exception:
            await self.repository.session.rollback()
            raise

        # DB 삭제가 성공한 후 실제 X-Ray 파일도 삭제
        for file_path in xray_file_paths:
            try:
                file_path.unlink(missing_ok=True)
            except OSError as error:
                raise RuntimeError(
                    "환자 삭제 후 X-Ray 이미지 파일 삭제에 실패했습니다."
                ) from error

    # 환자 목록 조회
    async def get_patients(
        self,
        current_user: User,
        name: str | None = None,
        gender: Gender | None = None,
        min_age: int | None = None,
        max_age: int | None = None,
    ) -> list[Patient]:
        has_allowed_role = current_user.role in {Role.STAFF, Role.ADMIN}
        has_allowed_department = current_user.department in {
            Department.DEV,
            Department.MEDICAL,
            Department.RESEARCH,
        }

        if not (has_allowed_role and has_allowed_department):
            raise PermissionError("환자 목록 조회 권한이 없습니다.")

        if (
            min_age is not None
            and max_age is not None
            and min_age > max_age
        ):
            raise ValueError("최소 나이는 최대 나이보다 클 수 없습니다.")

        return await self.repository.find_all(
            name=name,
            gender=gender,
            min_age=min_age,
            max_age=max_age,
        )
