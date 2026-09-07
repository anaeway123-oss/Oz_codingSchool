# 4. Git & GitHub Branch 전략

## 무엇을 진행했는가

OZ 3조는 여러 팀원이 동시에 작업할 때 서로의 코드를 직접 덮어쓰거나
완성되지 않은 기능이 바로 `main`에 들어가는 것을 방지하기 위해
`feature → integration → main` 흐름으로 Git 브랜치를 운영했습니다.

각 팀원은 자신의 담당 기능이나 문서를 개인 `feature` 브랜치에서 작업하고,
완료 후 Pull Request를 통해 해당 일차의 `integration` 브랜치에 먼저 병합했습니다.

팀원 작업이 모두 모인 뒤에는 통합 브랜치에서 전체 변경 내용과 실행 결과를 확인하고,
마지막으로 `integration → main` Pull Request를 생성해 최종 결과를 반영했습니다.

## 실제 사용한 브랜치 흐름

- `feature`: 각 팀원이 자신의 담당 작업을 진행하는 개인 작업 공간
- `integration`: 여러 팀원의 결과물을 먼저 모아 통합 검증하는 공용 작업 공간
- `main`: 최종 검토와 테스트가 끝난 결과만 반영하는 완성본 브랜치

실제 흐름:

    feature branch
        ↓
    Pull Request / 리뷰
        ↓
    integration branch
        ↓
    통합 테스트 및 QA
        ↓
    최종 Pull Request
        ↓
    main

실제 사용 예시:

- Docker 2일차: `integration/day2-event-driven-merge`
- Docker 3일차: `integration/day3-redis-worker-merge`
- Docker 3일차 애영님 최종 통합: `feature/day3-aeyoung-final-integration`
- Docker 4일차: `integration/day4-readme-merge`
- Docker 4일차 애영님 개인 작업: `feature/day4-aeyoung-git-qa`

## PR 및 Merge 원칙

1. 작업 시작 전 현재 브랜치와 `git status`를 먼저 확인했습니다.
2. 각 담당자는 자신의 `feature` 브랜치에서만 작업했습니다.
3. 작업 완료 후 바로 `main`으로 보내지 않고 먼저 `integration`으로 PR을 생성했습니다.
4. PR의 변경 파일과 담당 범위가 맞는지 확인한 뒤 Merge했습니다.
5. 충돌이나 예상하지 못한 변경이 발견되면 임의로 해결하지 않고 원인을 먼저 확인했습니다.
6. 최종 통합과 테스트가 끝난 뒤에만 `integration → main` PR을 생성했습니다.
7. `.env`, 비밀번호, 토큰 등 민감정보가 Git에 포함되지 않도록 확인했습니다.

## 3일차에서 적용한 실제 협업 흐름

Docker 3일차는 작업 간 의존성이 있어 순차적으로 진행했습니다.

    성규님 Redis Service
        ↓
    수빈님 FastAPI ↔ Redis
        ↓
    효민님 AI Worker
        ↓
    애영님 Docker 최종 통합 및 QA
        ↓
    integration/day3-redis-worker-merge
        ↓
    main

각 담당자의 PR이 `integration/day3-redis-worker-merge`에 병합된 뒤
다음 담당자가 최신 integration을 기준으로 작업하도록 하여
이전 작업을 누락하거나 오래된 브랜치에서 개발하는 문제를 줄였습니다.

애영님 최종 통합 단계에서는 Docker Compose에 AI Worker를 연결하고,
FastAPI / MySQL / Redis / AI Worker 전체 실행과
Redis Queue → AI Worker → SimpleCNN → Pub/Sub 흐름을 검증했습니다.

최종 검증 후 `integration/day3-redis-worker-merge → main` PR을 통해
Docker 3일차 결과를 최종 반영했습니다.

## 4일차에서 적용하는 협업 방식

Docker 4일차는 새 기능 구현보다 문서 정리가 중심이므로
3일차와 달리 각 팀원이 서로 다른 초안 파일을 동시에 작성할 수 있도록 구성했습니다.

각 팀원은 최신 `integration/day4-readme-merge`에서 자신의 feature 브랜치를 만들고,
`docs/day4_parts/` 아래 자신의 초안 파일만 작성합니다.

개인 PR은 모두 `integration/day4-readme-merge`로 병합하고,
모든 초안이 모이면 애영님이 최종 `README.md` 통합과 QA를 진행합니다.

## 진행 방식 선택 이유

이 브랜치 전략을 사용한 가장 큰 이유는
여러 팀원이 동시에 작업하더라도 서로의 변경을 최대한 안전하게 분리하고,
완성되지 않은 코드가 바로 `main`에 들어가는 것을 방지하기 위해서입니다.

또한 Pull Request와 integration 브랜치를 중간 검토 단계로 사용하면서
각 담당자의 변경 범위와 테스트 결과를 확인한 뒤 최종본에 반영할 수 있었습니다.

## 확인 및 테스트 결과

- Docker 작업에서는 feature → integration → main 흐름을 중심으로 협업했습니다.
- Docker 3일차의 팀원 PR과 최종 통합 PR을 확인한 뒤 `main`까지 Merge했습니다.
- Docker 4일차용 `integration/day4-readme-merge` 브랜치를 최신 `main`에서 생성했습니다.
- 현재 애영님 개인 브랜치 `feature/day4-aeyoung-git-qa`에서 이 초안을 작성하고 있습니다.

## 한 줄 회고

기능 구현뿐 아니라 브랜치와 PR 흐름을 명확하게 나누는 것이
여러 사람이 함께 작업할 때 코드를 안전하게 통합하는 중요한 협업 과정임을 배웠습니다.

---

# 10. QA

Docker 4일차 최종 통합 단계에서 팀원별 작성 내용과 기존 구현 결과를 기준으로
로컬 Docker 환경에서 주요 서비스와 AI 예측 전체 흐름을 최종 확인했습니다.

## QA 진행 내용

1. Docker 서비스 상태 확인
   - FastAPI, MySQL, Redis, AI Worker 컨테이너가 정상 실행되는 것을 확인했습니다.
   - FastAPI, MySQL, Redis의 정상 상태를 확인했습니다.

2. Swagger 및 인증 확인
   - `http://127.0.0.1:8000/docs` Swagger UI가 정상적으로 열리는 것을 확인했습니다.
   - Docker 환경의 MySQL은 9월 2일 생성된 별도 volume을 사용하고 있어,
     이전 API 실습에서 사용했던 테스트 계정이 현재 Docker DB에는 존재하지 않음을 확인했습니다.
   - QA용 의료 실무진 계정을 회원가입한 뒤 로컬 QA 환경에서 STAFF 권한을 설정했습니다.
   - `POST /auth/login` 요청이 `200 OK`로 정상 동작하는 것을 확인했습니다.

3. 환자 및 진료기록 생성 확인
   - 인증된 STAFF / MEDICAL 계정으로 환자 목록 조회가 `200 OK`로 동작함을 확인했습니다.
   - QA용 환자 생성 요청이 `201 Created`로 정상 처리됨을 확인했습니다.
   - 흉부 X-ray PNG 파일을 포함한 진료기록 생성 요청이 `201 Created`로 처리되고,
     X-ray 이미지 경로가 함께 저장되는 것을 확인했습니다.

4. AI 폐렴 예측 및 결과 저장 확인
   - 생성된 환자와 진료기록을 대상으로 AI 폐렴 예측 API를 실행했습니다.
   - `POST /patients/{patient_id}/medical-records/{record_id}/ai-predictions`
     요청이 `200 OK`로 정상 처리됨을 확인했습니다.
   - SimpleCNN 모델의 폐렴 예측 결과가 반환되었으며,
     `is_pneumonia`, `confidence`, `ai_model`, `created_at` 등의 값이 정상 응답되는 것을 확인했습니다.
   - 이번 구현 범위에서 Heatmap은 사용하지 않으므로 `heatmap_url`은 `null`로 반환됨을 확인했습니다.

5. DB 저장 및 조회 확인
   - `GET /patients/{patient_id}/medical-records/{record_id}/ai-predictions`
     요청을 통해 직전에 생성된 AI 예측 결과가 DB에서 정상 조회되는 것을 확인했습니다.
   - POST 예측 결과와 GET 조회 결과의 `id`, `record_id`, 예측값 및 생성 시간이 동일함을 확인했습니다.

6. 동일 요청 캐시 동작 확인
   - 동일한 환자와 진료기록에 AI 예측 POST 요청을 다시 실행했습니다.
   - 새로운 결과가 추가 생성되지 않고 기존 결과의 동일한 `id`와 `created_at`이 반환되는 것을 확인했습니다.
   - 이를 통해 동일 진료기록의 기존 AI 예측 결과를 재사용하는 흐름이 정상 동작함을 확인했습니다.

## 최종 QA 결과

- Docker 서비스 실행: PASS
- Swagger API 접근: PASS
- 회원가입 및 로그인: PASS
- 환자 생성: PASS
- X-ray 포함 진료기록 생성: PASS
- AI 폐렴 예측: PASS
- AI 예측 결과 DB 저장 및 조회: PASS
- 동일 요청 기존 결과 재사용: PASS

Docker 3일차에서 확인했던
`Redis Queue → AI Worker → SimpleCNN → Redis Pub/Sub` 흐름과 함께,
이번 최종 QA에서는 실제 HTTP 요청부터 AI 예측 결과 저장, 조회 및 재사용까지의
전체 서비스 흐름이 정상적으로 연결되는 것을 확인했습니다.

## 한 줄 회고

각 기능을 개별적으로 구현하는 것뿐 아니라 실제 사용자 요청부터 AI 예측,
DB 저장과 재조회까지 전체 흐름을 직접 검증하면서
통합 QA의 중요성과 문제 원인을 단계적으로 좁혀가는 방법을 배웠습니다.
