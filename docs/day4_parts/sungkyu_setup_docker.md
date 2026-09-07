# 성규 - 프로젝트 세팅 및 Docker 인프라 정리

## 5. 프로젝트 세팅

### 무엇을 진행했는가

프로젝트는 FastAPI 애플리케이션과 MySQL 데이터베이스를 기본 실행 환경으로 구성하고,
Alembic을 이용해 애플리케이션 실행 시 데이터베이스 마이그레이션을 적용할 수 있도록 구성했습니다.

현재 프로젝트에는 다음과 같은 기본 설정 파일과 구조가 포함되어 있습니다.

- `pyproject.toml`, `uv.lock` : Python 패키지 및 의존성 관리
- `alembic.ini`, `alembic/` : DB 마이그레이션 관리
- `app/` : FastAPI 애플리케이션
- `worker/` : AI Worker 실행 코드
- `static/`, `media/` : 정적 파일 및 이미지 관련 영역

Docker 환경에서는 FastAPI 컨테이너 시작 시
`alembic upgrade head`를 먼저 실행한 뒤 Uvicorn 서버를 실행하도록 구성되어 있습니다.

### Dockerfile 구성

현재 `app/Dockerfile`은 다음과 같은 흐름으로 구성되어 있습니다.

- `python:3.13-slim` 기반 이미지 사용
- `gcc`, `python3-dev`, `curl` 등 필요한 시스템 패키지 설치
- `uv` 패키지 매니저 사용
- `pyproject.toml`, `uv.lock`을 이용한 의존성 설치
- `/app`을 작업 디렉터리로 사용
- 애플리케이션 및 Alembic 관련 파일 복사
- 8000 포트 사용
- Uvicorn으로 FastAPI 실행

의존성 파일을 먼저 복사한 뒤 애플리케이션 코드를 복사하는 방식으로 구성되어 있어
Docker 이미지 빌드 과정에서 의존성 레이어를 재사용하기 쉬운 구조입니다.

---

## 8. Docker 인프라 관련 파일 작성

### `.dockerignore`

현재 프로젝트 루트의 `.dockerignore`에서 Docker 이미지 빌드에 필요하지 않은 파일을 제외하고 있습니다.

주요 제외 대상은 다음과 같습니다.

- Python 캐시
- `.env` 등 환경변수 및 민감 파일
- `.venv` 등 가상환경
- 테스트 및 도구 캐시
- 로그 파일
- IDE / OS 설정 파일
- Git 관련 파일
- Docker 이미지 실행에 필요하지 않은 문서 파일

이를 통해 불필요한 파일이나 민감정보가 Docker build context에 포함되는 것을 줄이도록 구성했습니다.

### `docker-compose.yml`

현재 Docker Compose 환경은 다음 4개 서비스로 분리되어 있습니다.

- `fastapi`
- `ai-worker`
- `mysql`
- `redis`

#### FastAPI

FastAPI 서비스는 웹 API 요청을 처리합니다.

MySQL과 Redis 접속 정보를 환경변수로 전달받으며,
MySQL과 Redis가 healthcheck를 통과한 이후 실행할 수 있도록 의존 관계가 설정되어 있습니다.

#### MySQL

MySQL 8.0 이미지를 사용하며 애플리케이션의 데이터 저장소 역할을 합니다.

`mysqladmin ping`을 이용한 healthcheck가 설정되어 있어
DB가 정상적으로 요청을 받을 수 있는 상태인지 확인할 수 있습니다.

#### Redis

Docker 3일차에서 Redis 기본 환경 구성을 담당했습니다.

- 서비스 이름: `redis`
- 이미지: `redis:7-alpine`
- healthcheck: `redis-cli ping`
- FastAPI와 AI Worker 사이의 작업 전달을 지원하는 Redis 환경 제공

Redis 컨테이너 실행 후 다음 결과를 실제로 확인했습니다.

- `docker compose config --quiet` : 오류 없이 통과
- `docker compose up -d redis` : Redis 컨테이너 실행 성공
- `docker compose ps redis` : `Up (healthy)` 확인
- `docker compose exec redis redis-cli ping` : `PONG` 확인

#### AI Worker

AI Worker는 FastAPI와 분리된 별도 서비스로 구성되어 있으며,
`python worker/main.py` 명령으로 실행됩니다.

Redis에 의존하도록 구성되어 있어 Redis가 정상 상태가 된 뒤 Worker가 실행될 수 있는 구조입니다.

---

## 진행 방식 및 선택 이유

Docker Compose를 이용해 FastAPI, MySQL, Redis, AI Worker를 각각 독립된 서비스로 분리함으로써
서비스별 역할과 실행 상태를 명확하게 확인할 수 있도록 구성했습니다.

특히 Redis는 FastAPI와 AI Worker 사이의 작업 처리 구조를 연결하기 위한 기반 서비스이므로,
별도의 healthcheck를 추가해 실제 명령에 응답할 수 있는 상태인지 확인했습니다.

Docker 4일차에서는 기존 설정을 새로 변경하지 않고,
현재 프로젝트에 실제 반영된 Docker 구조와 이전 작업에서 확인한 실행 결과를 기준으로 문서화했습니다.

---

## 확인 / 테스트 결과

Docker 3일차 Redis 환경 구성 과정에서 Redis 컨테이너가 `healthy` 상태로 실행되는 것을 확인했고,
`redis-cli ping` 명령에 `PONG`이 반환되는 것을 확인했습니다.

또한 변경 범위를 확인해 기존 FastAPI / MySQL / Alembic 설정을 의도치 않게 수정하지 않았음을 확인했습니다.

---

## 한 줄 회고

Docker Compose를 통해 여러 서비스를 분리하고 healthcheck와 의존 관계를 설정하면,
각 서비스의 역할과 실행 상태를 훨씬 명확하게 관리할 수 있다는 점을 배웠습니다.