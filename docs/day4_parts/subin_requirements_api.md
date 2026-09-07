# 사용자 요구사항 및 API 명세

## 문서 개요

이 문서는 AI 폐렴 진단 지원 서비스의 사용자 요구사항과 주요 API 명세를 실제 구현 코드를 기준으로 정리한 초안입니다. 사용자 계정 관리, 환자 관리, 진료기록 및 X-ray 관리, AI 폐렴 예측 기능의 동작과 연결 관계를 설명합니다.

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

## 작성 기준 및 확인 결과

### 실제 확인한 파일

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

### 확인 결과

- FastAPI 앱에 등록된 실제 라우터의 Method와 Path를 확인했습니다.
- OpenAPI 스키마를 통해 요청 본문 형식과 기본 성공·검증 응답 코드를 확인했습니다.
- API, Schema, Service 코드를 비교하여 권한, 입력값, 응답 필드 및 예외 처리를 정리했습니다.
- 연습용 `/practice_api` 엔드포인트는 실제 서비스 API 명세에서 제외했습니다.
- 이 문서는 코드 실행 결과를 새로 주장하는 테스트 보고서가 아니라, 현재 구현된 코드와 Swagger 명세를 기준으로 작성한 README 통합용 초안입니다.

> 사용자 요구사항과 API 명세를 실제 구현 코드에 맞춰 정리하면서 FastAPI, Redis, AI Worker 및 데이터베이스가 연결되는 전체 흐름을 다시 이해할 수 있었습니다.