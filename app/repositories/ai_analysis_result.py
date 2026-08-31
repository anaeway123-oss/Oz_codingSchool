from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_analysis_result import AiAnalysisResult


class AiAnalysisResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # 같은 진료기록 + 같은 AI 모델의 기존 예측 결과 조회
    async def find_by_record_and_model(
        self,
        record_id: int,
        ai_model: str,
    ) -> AiAnalysisResult | None:
        result = await self.session.execute(
            select(AiAnalysisResult).where(
                AiAnalysisResult.record_id == record_id,
                AiAnalysisResult.ai_model == ai_model,
            )
        )

        return result.scalar_one_or_none()

    # 특정 진료기록의 AI 예측 결과 목록 조회
    async def find_all_by_record_id(
        self,
        record_id: int,
    ) -> list[AiAnalysisResult]:
        result = await self.session.execute(
            select(AiAnalysisResult)
            .where(AiAnalysisResult.record_id == record_id)
            .order_by(AiAnalysisResult.created_at.desc())
        )

        return list(result.scalars().all())

    # 새 AI 예측 결과를 세션에 추가
    def add(
        self,
        analysis_result: AiAnalysisResult,
    ) -> None:
        self.session.add(analysis_result)

    # DB 저장 확정
    async def commit(self) -> None:
        await self.session.commit()

    # 저장 후 생성된 ID와 값을 다시 읽기
    async def refresh(
        self,
        analysis_result: AiAnalysisResult,
    ) -> None:
        await self.session.refresh(analysis_result)

    # 오류 발생 시 작업 취소
    async def rollback(self) -> None:
        await self.session.rollback()
