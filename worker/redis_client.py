import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

PREDICTION_TASK_QUEUE = "pneumonia:tasks"
PREDICTION_RESULT_CHANNEL_PREFIX = "pneumonia:results"


def get_redis_client() -> redis.Redis:
    """Worker 전용 동기 Redis Client 인스턴스를 반환합니다."""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )


def get_result_channel(task_id: str) -> str:
    """특정 작업 ID에 대응하는 결과 Publish 채널명을 반환합니다."""
    return f"{PREDICTION_RESULT_CHANNEL_PREFIX}:{task_id}"
