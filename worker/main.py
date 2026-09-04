import json
import logging
import sys
from pathlib import Path

# 프로젝트 루트 경로 등록
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from worker.model import predict_pneumonia
from worker.redis_client import (
    PREDICTION_TASK_QUEUE,
    get_redis_client,
    get_result_channel,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)
logger = logging.getLogger("AIWorker")


def run_worker():
    client = get_redis_client()
    logger.info("AI Worker 시작 - Redis 연결 완료")
    logger.info(f"대기열 '{PREDICTION_TASK_QUEUE}' 작업 대기 중...")

    while True:
        try:
            item = client.brpop(PREDICTION_TASK_QUEUE, timeout=0)
            if not item:
                continue

            _, raw_payload = item
            logger.info(f"작업 수신: {raw_payload}")

            try:
                task_data = json.loads(raw_payload)
            except Exception as e:
                logger.error(f"JSON 파싱 실패: {e}")
                continue

            task_id = task_data.get("task_id")
            image_path = task_data.get("image_path")

            if not task_id or not image_path:
                logger.error(f"필수 필드 누락: task_id={task_id}, image_path={image_path}")
                continue

            result_channel = get_result_channel(task_id)

            try:
                prediction = predict_pneumonia(image_path)
                result_payload = {
                    "task_id": task_id,
                    "status": "success",
                    "is_pneumonia": prediction["is_pneumonia"],
                    "confidence": prediction["confidence"],
                }
                logger.info(f"추론 성공 (Task: {task_id}): {result_payload}")
            except Exception as exc:
                logger.error(f"추론 실패 (Task: {task_id}): {exc}")
                result_payload = {
                    "task_id": task_id,
                    "status": "failed",
                    "error": str(exc),
                }

            client.publish(
                result_channel,
                json.dumps(result_payload, ensure_ascii=False),
            )
            logger.info(f"채널 '{result_channel}' 발행 완료")

        except KeyboardInterrupt:
            logger.info("AI Worker를 종료합니다.")
            break
        except Exception as e:
            logger.error(f"Worker 예외 발생: {e}")


if __name__ == "__main__":
    run_worker()
