from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.medical_record import MedicalRecordService


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class XrayNotFoundError(ValueError):
    pass


class XrayFileNotFoundError(FileNotFoundError):
    pass


class PredictionModelUnavailableError(RuntimeError):
    pass


class PredictionIntegrationService:
    def __init__(self, session: AsyncSession):
        self.medical_record_service = MedicalRecordService(session)

    async def predict_medical_record(
        self,
        patient_id: int,
        record_id: int,
    ) -> dict[str, int | str | bool | float]:
        # 1. Get the medical record and its related X-ray information.
        medical_record = (
            await self.medical_record_service.get_medical_record_detail(
                patient_id=patient_id,
                record_id=record_id,
            )
        )

        # 2. A prediction cannot run without an X-ray.
        if not medical_record.xray_images:
            raise XrayNotFoundError(
                "진료기록에 연결된 X-Ray 이미지가 없습니다."
            )

        xray = medical_record.xray_images[0]

        # 3. Convert the stored URL to a real local file path.
        image_path = (
            BASE_DIR / xray.image_url.lstrip("/\\")
        ).resolve()

        if not image_path.is_file():
            raise XrayFileNotFoundError(
                "저장된 X-Ray 이미지 파일을 찾을 수 없습니다."
            )

        # 4. Import the AI model only when prediction is actually requested.
        # The model code is currently being developed on another team branch.
        try:
            from worker.model import predict_pneumonia
        except (ImportError, ModuleNotFoundError) as error:
            raise PredictionModelUnavailableError(
                "폐렴 예측 모델을 불러올 수 없습니다."
            ) from error

        # 5. Pass the real X-ray file path to the team's prediction function.
        return predict_pneumonia(image_path)
