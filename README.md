# AI Health Web Assignment

## 1. Team Rule 정의

### 무엇을 진행했는가
팀 프로젝트를 진행하면서 실제로 사용한 협업 규칙을 정리했습니다.
여러 명이 동시에 기능을 개발하는 과정에서 작업 범위가 겹치거나 코드가 충돌하는 문제를 줄이기 위해 브랜치, PR, 담당 범위, 민감정보 관리 기준을 정하고 이를 기준으로 협업했습니다.

### 실제 사용한 Team Rule

#### 1. 개인 작업은 feature 브랜치에서 진행
각자 맡은 기능은 개인 feature 브랜치에서 작업했습니다.
통합 브랜치나 main 브랜치를 직접 수정하지 않고 작업 범위를 분리해 다른 팀원의 변경사항과 충돌할 가능성을 줄였습니다.

#### 2. 작업 완료 후 PR을 통해 integration 브랜치에 반영
기능 구현이 완료되면 바로 main에 반영하지 않고 PR을 생성했습니다.
PR에서 변경 파일과 작업 내용을 확인한 뒤 integration 브랜치에 Merge하고, 여러 기능이 정상적으로 합쳐진 뒤 최종적으로 main에 반영하는 방식을 사용했습니다.

#### 3. 담당 범위를 벗어난 파일은 임의로 수정하지 않기
각자 맡은 기능과 파일을 중심으로 작업했습니다.
다른 담당자의 코드 수정이 필요한 경우 혼자 판단해 변경하기보다 팀원에게 먼저 상황을 공유하고 수정 범위를 확인한 뒤 진행했습니다.

#### 4. Conflict 발생 시 임의로 해결하지 않고 공유
브랜치 Merge 과정에서 Conflict가 발생하면 한쪽 코드를 임의로 삭제하거나 덮어쓰지 않고 팀원과 변경 내용을 먼저 확인했습니다.
어떤 코드를 유지해야 하는지 확인한 뒤 충돌을 해결하는 방식으로 코드 유실을 방지했습니다.

#### 5. 민감정보는 Git 저장소에 포함하지 않기
`.env`, 비밀번호, API Key, Token 등 외부에 노출되면 안 되는 정보는 Git에 직접 올리지 않는 것을 원칙으로 했습니다.
공유가 필요한 환경 변수는 실제 값 대신 예시 형태로 관리했습니다.

### 진행 방식 또는 선택 이유
여러 명이 동시에 하나의 프로젝트를 개발할 때는 기능 구현 자체뿐만 아니라 변경사항을 안전하게 합치는 과정도 중요하다고 생각했습니다.
그래서 `feature → integration → main` 흐름을 사용하고, 각자의 작업 범위와 변경 내용을 PR 단위로 확인하도록 했습니다.

이 방식으로 각 담당자의 작업을 독립적으로 진행하면서도 최종 통합 과정에서 어떤 변경이 들어오는지 확인할 수 있었고, 충돌이나 예상하지 못한 코드 변경을 줄일 수 있었습니다.

### 확인 결과
- 각 담당자의 작업을 개인 브랜치와 PR 단위로 관리했습니다.
- integration 브랜치에서 기능을 먼저 통합한 뒤 main으로 반영하는 흐름을 사용했습니다.
- Merge 전 변경 파일과 작업 내용을 확인했습니다.
- 민감정보와 담당 외 파일이 불필요하게 포함되지 않도록 확인했습니다.

### 한 줄 회고
협업에서는 코드를 빠르게 작성하는 것만큼 작업 범위와 변경 과정을 팀원끼리 명확하게 공유하는 것이 중요하다는 점을 배웠습니다.

## 2. 사용자 요구사항

### 2.1 사용자 계정 및 인증

- 사용자는 이메일, 비밀번호, 이름, 부서, 성별, 휴대폰 번호를 입력하여 회원가입할 수 있어야 합니다.
- 사용자는 이메일과 비밀번호로 로그인할 수 있어야 합니다.
- 로그인 성공 시 Access Token을 응답으로 받고, Refresh Token은 JavaScript에서 접근할 수 없는 HTTP-only 쿠키로 전달되어야 합니다.
- 사용자는 Refresh Token을 이용해 Access Token을 재발급받을 수 있어야 합니다.
- 사용자는 로그아웃하거나 자신의 계정을 탈퇴할 수 있어야 합니다.
- 로그인한 사용자는 자신의 정보와 권한을 조회할 수 있어야 합니다.
- 로그인한 사용자는 자신의 부서와 휴대폰 번호만 부분 수정할 수 있어야 합니다.
- 로그인한 사용자는 현재 비밀번호를 확인한 후 비밀번호를 변경할 수 있어야 합니다.
- 관리자는 전체 사용자 목록을 조회하고 사용자의 권한을 변경할 수 있어야 합니다.

### 2.2 환자 관리

- 승인된 사용자는 환자 목록을 조회할 수 있어야 합니다.
- 환자 목록은 이름, 성별, 최소 나이, 최대 나이를 기준으로 검색하거나 필터링할 수 있어야 합니다.
- 의료 부서의 승인된 사용자는 환자 정보를 등록할 수 있어야 합니다.
- 승인된 사용자는 환자의 상세 정보를 조회하고 환자의 이름과 휴대폰 번호를 수정할 수 있어야 합니다.
- 승인된 사용자는 환자를 삭제할 수 있어야 하며, 관련 진료기록과 X-ray 파일도 함께 처리되어야 합니다.
- 존재하지 않는 환자를 요청하면 적절한 오류 응답을 제공해야 합니다.

### 2.3 진료기록 및 X-ray 관리

- 의료 부서의 승인된 실무진은 환자에게 진료기록을 등록할 수 있어야 합니다.
- 진료기록 등록 시 차트번호, 증상, 흉부 X-ray 이미지를 함께 전달해야 합니다.
- X-ray 파일은 JPG, JPEG, PNG 형식만 허용해야 합니다.
- 승인된 사용자는 환자별 진료기록 목록과 상세 정보를 조회할 수 있어야 합니다.
- 진료기록 상세 정보에는 연결된 X-ray 이미지 정보가 포함되어야 합니다.
- 중복된 차트번호, 지원하지 않는 이미지 형식, 존재하지 않는 환자 등에 대해 적절한 오류를 반환해야 합니다.

### 2.4 AI 폐렴 예측

- 승인된 사용자와 관리자는 특정 환자의 진료기록에 연결된 X-ray 이미지로 폐렴 예측을 요청할 수 있어야 합니다.
- 예측 요청에는 `patient_id`와 `record_id`를 경로 매개변수로 사용하며 별도의 요청 본문은 사용하지 않습니다.
- 동일한 진료기록과 동일한 AI 모델의 결과가 이미 저장되어 있으면 모델을 다시 실행하지 않고 기존 결과를 반환해야 합니다.
- 새로운 예측이 필요하면 FastAPI가 작업 ID를 생성하고 예측 작업을 Redis Queue에 전달해야 합니다.
- AI Worker가 전달한 결과는 Redis Pub/Sub을 통해 수신하고 데이터베이스에 저장해야 합니다.
- 예측 결과에는 폐렴 여부, 신뢰도, 모델명, 생성 일시 등이 포함되어야 합니다.
- 사용자는 진료기록에 저장된 AI 예측 결과 목록을 조회할 수 있어야 합니다.
- X-ray 또는 실제 이미지 파일이 없으면 `404 Not Found`, Redis 또는 Worker 처리 실패 시 `503 Service Unavailable`, 결과 대기 시간 초과 시 `504 Gateway Timeout`을 반환해야 합니다.

## 3. API 명세서

모든 보호 API는 JWT Bearer Token 인증이 필요합니다. 아래 표는 연습용 `/practice_api`를 제외하고 실제 서비스에 등록된 API를 기준으로 작성했습니다.

### 3.1 사용자 및 인증 API

| Method | Path | 요청 데이터 | 주요 기능 | 성공 코드 |
| --- | --- | --- | --- | --- |
| `POST` | `/users/signup` | JSON: `email`, `password`, `name`, `department`, `gender`, `phone_number` | 회원가입 | `201` |
| `POST` | `/auth/login` | JSON: `email`, `password` | 로그인 및 토큰 발급 | `200` |
| `POST` | `/auth/refresh` | HTTP-only 쿠키의 `refresh_token` | Access Token 재발급 | `200` |
| `POST` | `/auth/logout` | 요청 본문 없음 | Refresh Token 쿠키 삭제 | `200` |
| `GET` | `/users/me` | 요청 본문 없음 | 로그인 사용자 본인 정보 조회 | `200` |
| `PATCH` | `/users/me` | JSON: `department`, `phone_number` 중 변경할 항목 | 본인 정보 부분 수정 | `200` |
| `PATCH` | `/users/me/password` | JSON: `current_password`, `new_password` | 본인 비밀번호 변경 | `200` |
| `DELETE` | `/users/me` | 요청 본문 없음 | 본인 계정 탈퇴 | `204` |
| `GET` | `/users` | Query: `query`, `department` 선택 | 관리자용 사용자 목록 조회 | `200` |
| `PATCH` | `/users/{user_id}/role` | JSON: `role` | 관리자용 사용자 권한 변경 | `200` |

### 3.2 환자 API

| Method | Path | 요청 데이터 | 주요 기능 | 성공 코드 |
| --- | --- | --- | --- | --- |
| `GET` | `/patients` | Query: `name`, `gender`, `min_age`, `max_age` 선택 | 환자 목록 조회·검색·필터링 | `200` |
| `POST` | `/patients` | JSON: `name`, `age`, `gender`, `phone` | 환자 등록 | `201` |
| `GET` | `/patients/{patient_id}` | Path: `patient_id` | 환자 상세 조회 | `200` |
| `PATCH` | `/patients/{patient_id}` | JSON: `name`, `phone` 중 변경할 항목 | 환자 정보 부분 수정 | `200` |
| `DELETE` | `/patients/{patient_id}` | Path: `patient_id` | 환자 및 관련 데이터 삭제 | `204` |

### 3.3 진료기록 및 X-ray API

| Method | Path | 요청 데이터 | 주요 기능 | 성공 코드 |
| --- | --- | --- | --- | --- |
| `POST` | `/patients/{patient_id}/medical-records` | Form: `chart_number`, `symptoms`, `xray_image` | 진료기록 등록 및 X-ray 업로드 | `201` |
| `GET` | `/patients/{patient_id}/medical-records` | Path: `patient_id` | 환자별 진료기록 목록 조회 | `200` |
| `GET` | `/patients/{patient_id}/medical-records/{record_id}` | Path: `patient_id`, `record_id` | 진료기록 및 X-ray 상세 조회 | `200` |

### 3.4 AI 폐렴 예측 API

| Method | Path | 요청 데이터 | 주요 기능 | 성공 코드 |
| --- | --- | --- | --- | --- |
| `POST` | `/patients/{patient_id}/medical-records/{record_id}/ai-predictions` | Path: `patient_id`, `record_id`; 요청 본문 없음 | AI 폐렴 예측 실행 또는 기존 결과 반환 | `200` |
| `GET` | `/patients/{patient_id}/medical-records/{record_id}/ai-predictions` | Path: `patient_id`, `record_id`; 요청 본문 없음 | 저장된 AI 예측 결과 목록 조회 | `200` |

### 3.5 AI 폐렴 예측 API 상세 명세

#### 3.5.1 폐렴 예측 실행

- **Method:** `POST`
- **Path:** `/patients/{patient_id}/medical-records/{record_id}/ai-predictions`
- **인증:** JWT Bearer Token 필수
- **권한:** 승인된 `STAFF` 또는 `ADMIN`
- **Request Body:** 없음

#### Path Parameters

| 이름 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `patient_id` | integer | 필수 | 예측 대상 환자의 ID |
| `record_id` | integer | 필수 | X-ray가 연결된 진료기록의 ID |

#### 요청 예시

```http
POST /patients/1/medical-records/10/ai-predictions
Authorization: Bearer {access_token}
```

#### 성공 응답 예시

```json
{
  "id": 3,
  "record_id": 10,
  "is_pneumonia": true,
  "confidence": 0.95,
  "heatmap_url": null,
  "ai_model": "SimpleCNN",
  "created_at": "2026-09-07T10:30:00"
}
```

#### 실제 처리 방식

1. 환자와 진료기록이 존재하고 서로 연결되어 있는지 확인합니다.
2. 같은 진료기록과 `SimpleCNN` 모델의 기존 결과가 있으면 재추론하지 않고 해당 결과를 반환합니다.
3. 기존 결과가 없으면 연결된 X-ray 정보와 실제 이미지 파일을 확인합니다.
4. 고유한 `task_id`를 생성하여 환자 ID, 진료기록 ID, 이미지 경로, 모델명을 Redis Queue에 전달합니다.
5. AI Worker가 처리한 결과를 Redis Pub/Sub으로 수신합니다.
6. 폐렴 여부와 신뢰도를 데이터베이스에 저장한 뒤 응답합니다.

#### 3.5.2 폐렴 예측 결과 목록 조회

- **Method:** `GET`
- **Path:** `/patients/{patient_id}/medical-records/{record_id}/ai-predictions`
- **인증:** JWT Bearer Token 필수
- **권한:** 승인된 `STAFF` 또는 `ADMIN`
- **Request Body:** 없음
- **성공 코드:** `200 OK`

#### 성공 응답 예시

```json
[
  {
    "id": 3,
    "record_id": 10,
    "is_pneumonia": true,
    "confidence": 0.95,
    "heatmap_url": null,
    "ai_model": "SimpleCNN",
    "created_at": "2026-09-07T10:30:00"
  }
]
```

저장된 결과가 없으면 빈 배열 `[]`을 반환할 수 있습니다.

#### 3.5.3 주요 상태 코드

| 상태 코드 | 의미 | 적용 예시 |
| --- | --- | --- |
| `200 OK` | 요청 처리 성공 | 예측 결과 생성·재사용 또는 목록 조회 성공 |
| `401 Unauthorized` | 인증 실패 | Access Token이 없거나 유효하지 않음 |
| `403 Forbidden` | 권한 부족 | 승인되지 않은 사용자가 예측 요청 |
| `404 Not Found` | 대상 또는 파일 없음 | 환자, 진료기록, X-ray 정보 또는 실제 이미지 파일이 없음 |
| `422 Unprocessable Entity` | 요청값 검증 실패 | 경로 매개변수 타입이 올바르지 않음 |
| `503 Service Unavailable` | Redis 또는 Worker 처리 실패 | Redis 연결 오류, Worker 실패, 잘못된 Worker 결과 |
| `504 Gateway Timeout` | 결과 대기 시간 초과 | 제한 시간 안에 Worker 결과를 받지 못함 |

### 3.6 구성 요소 연결 흐름

AI 폐렴 예측 요청은 다음 순서로 처리됩니다.

```text
사용자
→ FastAPI 예측 API
→ 환자·진료기록·X-ray 및 기존 결과 확인
→ Redis Task Queue
→ AI Worker의 SimpleCNN 예측
→ Redis Pub/Sub 결과 전달
→ FastAPI가 결과를 DB에 저장
→ 사용자에게 예측 결과 응답
```

각 구성 요소의 역할은 다음과 같습니다.

- **프론트엔드:** 환자 ID와 진료기록 ID를 포함한 예측 API를 호출하고 결과를 화면에 표시합니다.
- **FastAPI:** 인증·권한과 입력 정보를 확인하고 Redis에 예측 작업을 전달합니다.
- **Redis Queue:** AI Worker가 처리할 예측 작업을 임시로 보관합니다.
- **AI Worker:** X-ray 이미지를 전처리하고 SimpleCNN 모델로 폐렴 여부와 신뢰도를 계산합니다.
- **Redis Pub/Sub:** 작업 ID에 대응하는 Worker 결과를 FastAPI에 전달합니다.
- **데이터베이스:** 환자, 진료기록, X-ray 정보와 최종 AI 예측 결과를 저장합니다.

### 3.7 권한과 입력 검증 기준

- JWT 인증이 필요한 API는 유효한 Access Token이 없으면 사용할 수 없습니다.
- 관리자 API는 `ADMIN` 권한을 가진 사용자만 사용할 수 있습니다.
- 환자와 진료기록 API는 각 기능에 설정된 역할·부서 조건을 확인합니다.
- Pydantic 스키마와 FastAPI 매개변수 검증에 실패하면 일반적으로 `422 Unprocessable Entity`가 반환됩니다.
- 서비스 처리 중 대상이 없거나 권한이 부족한 경우 API 코드에 정의된 `400`, `403`, `404`, `409` 등의 오류가 반환됩니다.
- 비밀번호, Access Token, Refresh Token, 실제 `.env` 값은 문서에 기록하지 않습니다.

### 작성 기준 및 확인 결과

#### 실제 확인한 파일

- `app/apis/auth.py`
- `app/apis/user.py`
- `app/apis/mypage.py`
- `app/apis/user_delete.py`
- `app/apis/user_list.py`
- `app/apis/patient.py`
- `app/apis/medical_record.py`
- `app/apis/prediction.py`
- `app/schemas/user.py`
- `app/schemas/patient.py`
- `app/schemas/medical_record.py`
- `app/schemas/ai_analysis.py`
- `app/services/patient.py`
- `app/services/prediction.py`

#### 확인 결과

- FastAPI 앱에 등록된 실제 라우터의 Method와 Path를 확인했습니다.
- OpenAPI 스키마를 통해 요청 본문 형식과 기본 성공·검증 응답 코드를 확인했습니다.
- API, Schema, Service 코드를 비교하여 권한, 입력값, 응답 필드 및 예외 처리를 정리했습니다.
- 연습용 `/practice_api` 엔드포인트는 실제 서비스 API 명세에서 제외했습니다.
- 이 문서는 코드 실행 결과를 새로 주장하는 테스트 보고서가 아니라, 현재 구현된 코드와 Swagger 명세를 기준으로 작성한 README 통합용 초안입니다.

> 사용자 요구사항과 API 명세를 실제 구현 코드에 맞춰 정리하면서 FastAPI, Redis, AI Worker 및 데이터베이스가 연결되는 전체 흐름을 다시 이해할 수 있었습니다.

## 4. Git & GitHub Branch 전략

### 무엇을 진행했는가

OZ 3조는 여러 팀원이 동시에 작업할 때 서로의 코드를 직접 덮어쓰거나
완성되지 않은 기능이 바로 `main`에 들어가는 것을 방지하기 위해
`feature → integration → main` 흐름으로 Git 브랜치를 운영했습니다.

각 팀원은 자신의 담당 기능이나 문서를 개인 `feature` 브랜치에서 작업하고,
완료 후 Pull Request를 통해 해당 일차의 `integration` 브랜치에 먼저 병합했습니다.

팀원 작업이 모두 모인 뒤에는 통합 브랜치에서 전체 변경 내용과 실행 결과를 확인하고,
마지막으로 `integration → main` Pull Request를 생성해 최종 결과를 반영했습니다.

### 실제 사용한 브랜치 흐름

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

### PR 및 Merge 원칙

1. 작업 시작 전 현재 브랜치와 `git status`를 먼저 확인했습니다.
2. 각 담당자는 자신의 `feature` 브랜치에서만 작업했습니다.
3. 작업 완료 후 바로 `main`으로 보내지 않고 먼저 `integration`으로 PR을 생성했습니다.
4. PR의 변경 파일과 담당 범위가 맞는지 확인한 뒤 Merge했습니다.
5. 충돌이나 예상하지 못한 변경이 발견되면 임의로 해결하지 않고 원인을 먼저 확인했습니다.
6. 최종 통합과 테스트가 끝난 뒤에만 `integration → main` PR을 생성했습니다.
7. `.env`, 비밀번호, 토큰 등 민감정보가 Git에 포함되지 않도록 확인했습니다.

### 3일차에서 적용한 실제 협업 흐름

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

### 4일차에서 적용하는 협업 방식

Docker 4일차는 새 기능 구현보다 문서 정리가 중심이므로
3일차와 달리 각 팀원이 서로 다른 초안 파일을 동시에 작성할 수 있도록 구성했습니다.

각 팀원은 최신 `integration/day4-readme-merge`에서 자신의 feature 브랜치를 만들고,
`docs/day4_parts/` 아래 자신의 초안 파일만 작성합니다.

개인 PR은 모두 `integration/day4-readme-merge`로 병합하고,
모든 초안이 모이면 애영님이 최종 `README.md` 통합과 QA를 진행합니다.

### 진행 방식 선택 이유

이 브랜치 전략을 사용한 가장 큰 이유는
여러 팀원이 동시에 작업하더라도 서로의 변경을 최대한 안전하게 분리하고,
완성되지 않은 코드가 바로 `main`에 들어가는 것을 방지하기 위해서입니다.

또한 Pull Request와 integration 브랜치를 중간 검토 단계로 사용하면서
각 담당자의 변경 범위와 테스트 결과를 확인한 뒤 최종본에 반영할 수 있었습니다.

### 확인 및 테스트 결과

- Docker 작업에서는 feature → integration → main 흐름을 중심으로 협업했습니다.
- Docker 3일차의 팀원 PR과 최종 통합 PR을 확인한 뒤 `main`까지 Merge했습니다.
- Docker 4일차용 `integration/day4-readme-merge` 브랜치를 최신 `main`에서 생성했습니다.
- 현재 애영님 개인 브랜치 `feature/day4-aeyoung-git-qa`에서 이 초안을 작성하고 있습니다.

### 한 줄 회고

기능 구현뿐 아니라 브랜치와 PR 흐름을 명확하게 나누는 것이
여러 사람이 함께 작업할 때 코드를 안전하게 통합하는 중요한 협업 과정임을 배웠습니다.

---

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

## 6. API 및 AI Worker 코드 작성·병합
- 무엇을 진행했는가:
  - AI Worker 구현과 Event-Driven Architecture가 실제 서비스에 연결되는 전체 파이프라인을 구축했습니다.
  - 핵심 흐름: FastAPI → Redis Task Queue → AI Worker → SimpleCNN → Redis Pub/Sub → FastAPI → DB 저장으로 이어지는 데이터 통신 및 추론 과정을 구현했습니다.
- 실제 사용한 파일/기능/브랜치:
  - `worker/main.py`, `worker/redis_client.py`
  - 작업 브랜치: `feature/day4-hyomin-worker-architecture`
- 확인/테스트 결과:
  - FastAPI에서 전달된 작업이 Redis Queue를 거쳐 AI Worker(SimpleCNN)에서 처리되고, 다시 Redis Pub/Sub 채널로 반환되는 일련의 과정이 정상 동작함을 확인했습니다.

## 7. 아키텍처 설계 및 적용
- 진행 방식 또는 선택 이유:
  - 동기 처리 시 발생하는 API 서버 병목을 해결하기 위해 Redis 기반 비동기 메시지 큐 아키텍처를 적용했습니다.
  - 인프라 복잡도를 낮추기 위해 단일 Redis를 Task Queue와 Pub/Sub 채널로 동시에 활용하는 주요 결정을 내렸습니다.
- 한 줄 회고:
  - 아키텍처 설계 문서가 실제 코드로 연결되는 핵심 흐름을 직접 구현하며 Event-Driven 구조를 깊이 이해할 수 있었습니다.

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

### 진행 방식 및 선택 이유

Docker Compose를 이용해 FastAPI, MySQL, Redis, AI Worker를 각각 독립된 서비스로 분리함으로써
서비스별 역할과 실행 상태를 명확하게 확인할 수 있도록 구성했습니다.

특히 Redis는 FastAPI와 AI Worker 사이의 작업 처리 구조를 연결하기 위한 기반 서비스이므로,
별도의 healthcheck를 추가해 실제 명령에 응답할 수 있는 상태인지 확인했습니다.

Docker 4일차에서는 기존 설정을 새로 변경하지 않고,
현재 프로젝트에 실제 반영된 Docker 구조와 이전 작업에서 확인한 실행 결과를 기준으로 문서화했습니다.

---

### 확인 / 테스트 결과

Docker 3일차 Redis 환경 구성 과정에서 Redis 컨테이너가 `healthy` 상태로 실행되는 것을 확인했고,
`redis-cli ping` 명령에 `PONG`이 반환되는 것을 확인했습니다.

또한 변경 범위를 확인해 기존 FastAPI / MySQL / Alembic 설정을 의도치 않게 수정하지 않았음을 확인했습니다.

---

### 한 줄 회고

Docker Compose를 통해 여러 서비스를 분리하고 healthcheck와 의존 관계를 설정하면,
각 서비스의 역할과 실행 상태를 훨씬 명확하게 관리할 수 있다는 점을 배웠습니다.

## 9. AWS 배포

현재 단계에서는 AWS 배포를 완료한 것으로 기록하지 않으며, 다음 단계에서 실제 AWS 배포 및 검증을 진행할 예정입니다.

## 10. QA

Docker 4일차 최종 통합 단계에서 팀원별 작성 내용과 기존 구현 결과를 기준으로
로컬 Docker 환경에서 주요 서비스와 AI 예측 전체 흐름을 최종 확인했습니다.

### QA 진행 내용

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

### 최종 QA 결과

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

### 한 줄 회고

각 기능을 개별적으로 구현하는 것뿐 아니라 실제 사용자 요청부터 AI 예측,
DB 저장과 재조회까지 전체 흐름을 직접 검증하면서
통합 QA의 중요성과 문제 원인을 단계적으로 좁혀가는 방법을 배웠습니다.

## 부록. Alembic Migration Guide

이 프로젝트는 데이터베이스 마이그레이션을 위해 Alembic을 사용합니다.

### 1. 마이그레이션 파일 생성 (자동 생성)
모델(`app/models/`)이 변경된 경우 다음 명령어를 실행하여 마이그레이션 파일을 생성합니다.
```bash
uv run alembic revision --autogenerate -m "변경 내용 설명"
```

### 2. 데이터베이스에 반영
생성된 마이그레이션을 데이터베이스에 적용하려면 다음 명령어를 실행합니다.
```bash
uv run alembic upgrade head
```

### 3. 이전 상태로 되돌리기 (Rollback)
마지막 마이그레이션을 취소하려면 다음 명령어를 실행합니다.
```bash
uv run alembic downgrade -1
```
