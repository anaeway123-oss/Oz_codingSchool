# 1. Python 3.13 슬림 베이스 이미지 사용
FROM python:3.13-slim

# 2. C 확장 패키지(asyncmy 등) 빌드 도구 및 curl 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. uv 패키지 매니저 바이너리 복사
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 4. 컨테이너 작업 디렉터리 설정
WORKDIR /app

# 5. 의존성 파일 복사 및 설치 (도커 빌드 캐시 최적화)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 6. 가상환경 경로를 PATH 환경변수에 등록
ENV PATH="/app/.venv/bin:$PATH"

# 7. 애플리케이션 코드 복사
COPY app/ ./app
COPY static/ ./static
COPY alembic.ini ./
COPY alembic/ ./alembic/

# 8. 컨테이너 기본 실행 포트 및 명령 설정
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
