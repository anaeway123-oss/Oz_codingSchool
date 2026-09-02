# Docker 웹 서비스 배포 1일차 실행 증빙

## 1. 작업 개요

Docker 웹 서비스 배포 1일차에서 `.dockerignore` 작성 및 Docker 실행 증빙 정리를 담당합니다.

주요 확인 항목은 다음과 같습니다.

- `.dockerignore` 작성 및 제외 대상 검토
- Docker 이미지 빌드 성공 여부 확인
- FastAPI 컨테이너 실행 여부 확인
- MySQL 컨테이너 실행 및 health 상태 확인
- 필요 시 Docker 환경에서 API 정상 동작 확인

---

## 2. .dockerignore 작성

Docker 이미지에 불필요하거나 포함하면 안 되는 파일을 제외하기 위해 `.dockerignore`를 작성했습니다.

주요 제외 대상:

- Python 캐시 (`__pycache__`, `*.pyc` 등)
- 환경변수 및 민감 파일 (`.env`, `.env.*`)
- Python 가상환경 (`.venv`, `venv`)
- 테스트 및 도구 캐시
- 로그 파일
- IDE 설정 파일
- OS 임시 파일
- Git 관련 파일

애플리케이션 실행에 필요한 Python 소스와 디렉터리는 제외하지 않았습니다.

---

## 3. MySQL 컨테이너 실행 확인

`docker compose ps`와 `docker compose ps -a`를 통해 MySQL 컨테이너 상태를 확인했습니다.

확인 결과:

- Service: `mysql`
- Image: `mysql:8.0`
- Container: `oz_codingschool-mysql-1`
- Status: `Up (healthy)`
- Port: `3306`

MySQL 컨테이너가 정상 실행 중이며 health check도 통과한 상태를 확인했습니다.

### 실행 화면

![MySQL 컨테이너 healthy 상태](./images/docker_day1_mysql_healthy.png)

`docker compose ps` 실행 결과 MySQL 컨테이너가 `Up (healthy)` 상태로 정상 실행 중임을 확인했습니다.

---

## 4. FastAPI 컨테이너 실행 확인

현재 `integration/docker-day1-merge` 기준 `app/Dockerfile`이 아직 비어 있어 FastAPI Docker 이미지 빌드 및 컨테이너 실행 증빙은 팀 Dockerfile 통합 후 추가할 예정입니다.

### 추가 확인 예정

- Docker 이미지 빌드 성공
- FastAPI 컨테이너 실행
- FastAPI / MySQL 동시 실행 상태
- Docker 환경에서 API 또는 웹 서비스 정상 응답

---

## 5. 현재 진행 상태

- [x] `.dockerignore` 작성
- [x] 민감 파일 및 불필요 파일 제외 규칙 확인
- [x] 실행에 필요한 애플리케이션 파일 제외 여부 확인
- [x] MySQL 컨테이너 실행 및 healthy 상태 확인
- [ ] Docker 이미지 빌드 성공 화면
- [ ] FastAPI 컨테이너 실행 화면
- [ ] FastAPI / MySQL 연결 확인
- [ ] 최종 실행 증빙 이미지 추가

Dockerfile 통합 이후 남은 실행 테스트 및 캡처를 추가하여 최종 증빙 문서를 완성할 예정입니다.