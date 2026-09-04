import asyncio
import json
from typing import Any
from uuid import uuid4

from redis.asyncio import Redis

from app.core.config import settings


# FastAPI와 AI Worker가 공통으로 사용할 통신 규칙입니다.
PREDICTION_TASK_QUEUE = "pneumonia:tasks"
PREDICTION_RESULT_CHANNEL_PREFIX = "pneumonia:results"


# decode_responses=True로 설정하면 Redis 응답을 bytes가 아닌 문자열로 받습니다.
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def create_task_id() -> str:
    """동시에 들어온 예측 요청을 구분할 고유 ID를 생성합니다."""
    return str(uuid4())


def get_result_channel(task_id: str) -> str:
    """특정 작업의 결과만 받을 수 있는 Pub/Sub 채널명을 만듭니다."""
    return f"{PREDICTION_RESULT_CHANNEL_PREFIX}:{task_id}"

class PredictionResultTimeoutError(TimeoutError):
    """제한 시간 안에 Worker 결과를 받지 못한 경우 발생합니다."""


class PredictionWorkerError(RuntimeError):
    """Worker가 실패 결과를 전달한 경우 발생합니다."""


async def enqueue_prediction_and_wait(
    task_data: dict[str, Any],
) -> dict[str, Any]:
    """
    결과 채널을 먼저 구독하고 예측 작업을 Queue에 넣은 뒤,
    해당 task_id의 Worker 결과를 기다립니다.
    """
    task_id = str(task_data["task_id"])
    result_channel = get_result_channel(task_id)
    pubsub = redis_client.pubsub()

    try:
        # 작업 등록 전에 결과 채널부터 구독하여 빠른 결과를 놓치지 않습니다.
        await pubsub.subscribe(result_channel)

        # 구독 완료 응답을 확인한 다음 Queue에 작업을 등록합니다.
        try:
            async with asyncio.timeout(5):
                while True:
                    message = await pubsub.get_message(timeout=1.0)
                    if message and message["type"] == "subscribe":
                        break
        except TimeoutError as error:
            raise PredictionResultTimeoutError(
                "Redis 결과 채널 구독 시간이 초과되었습니다."
            ) from error

        await redis_client.lpush(
            PREDICTION_TASK_QUEUE,
            json.dumps(task_data, ensure_ascii=False),
        )

        try:
            async with asyncio.timeout(
                settings.REDIS_RESULT_TIMEOUT_SECONDS
            ):
                async for message in pubsub.listen():
                    if message["type"] != "message":
                        continue

                    try:
                        result = json.loads(message["data"])
                    except (json.JSONDecodeError, TypeError) as error:
                        raise PredictionWorkerError(
                            "Worker 결과가 올바른 JSON 형식이 아닙니다."
                        ) from error

                    if str(result.get("task_id")) != task_id:
                        continue

                    if result.get("status") == "failed":
                        raise PredictionWorkerError(
                            str(result.get("error", "AI 예측에 실패했습니다."))
                        )

                    if result.get("status") != "success":
                        raise PredictionWorkerError(
                            "Worker 결과의 상태값이 올바르지 않습니다."
                        )

                    if (
                        "is_pneumonia" not in result
                        or "confidence" not in result
                    ):
                        raise PredictionWorkerError(
                            "Worker 결과에 필수 예측값이 없습니다."
                        )

                    return result

        except TimeoutError as error:
            raise PredictionResultTimeoutError(
                "AI 예측 결과 대기 시간이 초과되었습니다."
            ) from error

    finally:
        await pubsub.unsubscribe(result_channel)
        await pubsub.aclose()