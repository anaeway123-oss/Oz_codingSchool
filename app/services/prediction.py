from decimal import Decimal
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_client import (
    create_task_id,
    enqueue_prediction_and_wait,
)
from app.models.ai_analysis_result import AiAnalysisResult
from app.repositories.ai_analysis_result import AiAnalysisResultRepository
from app.services.medical_record import MedicalRecordService


BASE_DIR = Path(__file__).resolve().parent.parent.parent
AI_MODEL_NAME = "SimpleCNN"


class XrayNotFoundError(ValueError):
    pass


class XrayFileNotFoundError(FileNotFoundError):
    pass

class PredictionIntegrationService:
    def __init__(self, session: AsyncSession):
        self.medical_record_service = MedicalRecordService(session)
        self.analysis_repository = AiAnalysisResultRepository(session)

    async def predict_medical_record(
        self,
        patient_id: int,
        record_id: int,
    ) -> AiAnalysisResult:
        # 1. 환자와 진료기록 확인
        medical_record = (
            await self.medical_record_service.get_medical_record_detail(
                patient_id=patient_id,
                record_id=record_id,
            )
        )

        # 2. 같은 진료기록 + 같은 AI 모델의 기존 결과 확인
        existing_result = (
            await self.analysis_repository.find_by_record_and_model(
                record_id=record_id,
                ai_model=AI_MODEL_NAME,
            )
        )

        # 기존 결과가 있다면 AI를 다시 실행하지 않고 반환
        if existing_result is not None:
            return existing_result

        # 3. 연결된 X-Ray 이미지 확인
        if not medical_record.xray_images:
            raise XrayNotFoundError(
                "진료기록에 연결된 X-Ray 이미지가 없습니다."
            )

        xray = medical_record.xray_images[0]

        # 4. 이미지의 실제 파일 경로 확인
        image_path = (
            BASE_DIR / xray.image_url.lstrip("/\\")
        ).resolve()

        if not image_path.is_file():
            raise XrayFileNotFoundError(
                "저장된 X-Ray 이미지 파일을 찾을 수 없습니다."
            )

        # 5. 동시에 들어온 요청과 결과를 구분할 고유 작업 ID 생성
        task_id = create_task_id()

        # 6. AI Worker가 예측에 사용할 작업 데이터 생성
        task_data = {
            "task_id": task_id,
            "patient_id": patient_id,
            "record_id": record_id,
            "image_path": str(image_path),
            "ai_model": AI_MODEL_NAME,
        }

        # 7. Redis Queue에 작업을 넣고 Worker의 Pub/Sub 결과 대기
        prediction = await enqueue_prediction_and_wait(task_data)

        # 8. 새로운 예측 결과 생성
        analysis_result = AiAnalysisResult(
            record_id=record_id,
            is_pneumonia=bool(prediction["is_pneumonia"]),
            confidence=Decimal(
                str(prediction["confidence"])
            ).quantize(Decimal("0.01")),
            heatmap_url=None,
            ai_model=AI_MODEL_NAME,
        )

        # 9. DB에 저장
        self.analysis_repository.add(analysis_result)

        try:
            await self.analysis_repository.commit()
            await self.analysis_repository.refresh(analysis_result)
        except Exception:
            await self.analysis_repository.rollback()
            raise

        return analysis_result

    async def get_prediction_results(
        self,
        patient_id: int,
        record_id: int,
    ) -> list[AiAnalysisResult]:
        # 환자와 진료기록 확인
        await self.medical_record_service.get_medical_record_detail(
            patient_id=patient_id,
            record_id=record_id,
        )

        # 해당 진료기록에 저장된 AI 예측 결과 목록 반환
        return await self.analysis_repository.find_all_by_record_id(
            record_id=record_id,
        )
