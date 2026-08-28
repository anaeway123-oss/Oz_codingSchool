from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Department, Role
from app.models.patient import Patient
from app.models.user import User
from app.repositories.patient import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


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
