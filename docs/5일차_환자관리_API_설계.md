# 5일차 환자관리 API 설계

## 1. 목적

5일차 사용자 요구사항 정의서를 기준으로 환자 관리 및 진료기록 API를 설계한다.

- 환자 관리: 등록, 목록 조회, 상세 조회, 수정, 삭제
- 진료기록: 등록, 목록 조회, 상세 조회
- 모든 API는 최대 3초 이내 응답을 목표로 한다.
- 요구사항표에는 진료기록 수정/삭제 요구사항이 명시되어 있지 않으므로 별도 요구사항 확인 전 임의로 추가하지 않는다.

## 2. 공통 원칙

- 기존 Patient / MedicalRecord / XrayImage / User 모델 구조를 최대한 유지한다.
- 로그인 사용자 인증은 기존 JWT 공통 인증 기능을 재사용한다.
- 권한 조건은 요구사항에 맞춰 적용한다.
- `.env`, 비밀번호, DB 접속 정보는 Git에 포함하지 않는다.
- 환자 삭제 시 관련 진료기록과 X-Ray 이미지도 함께 영구 삭제되는지 확인한다.
- X-Ray 이미지는 서버 실행 환경의 로컬 저장소에 저장한다.

## 3. API 명세

| 요구사항 ID | Method | Endpoint | 기능 | 권한/조건 | 주요 요청값 | 주요 응답값 |
|---|---|---|---|---|---|---|
| REQ-PTNT-001 | POST | `/patients` | 환자 정보 등록 | 사내 의료인 역할 | name, age, gender, phone_number | 생성된 환자 정보 |
| REQ-PTNT-002 | GET | `/patients` | 환자 목록 조회 | 로그인 된 사내 개발진/의료 실무진/연구진 | search(name), gender, min_age, max_age | id, name, age, gender, phone_number, created_at, updated_at |
| REQ-PTNT-003 | GET | `/patients/{patient_id}` | 환자 상세 조회 | 로그인 된 사내 개발진/의료 실무진/연구진 | patient_id | name, gender, phone_number, age |
| REQ-PTNT-004 | PATCH | `/patients/{patient_id}` | 환자 정보 수정 | 로그인 된 사내 개발진/의료 실무진/연구진 | name, phone_number 중 필요한 값 | 수정된 환자 정보 |
| REQ-PTNT-005 | DELETE | `/patients/{patient_id}` | 환자 정보 삭제 | 로그인 된 사내 개발진/의료 실무진/연구진 | patient_id + 삭제 확인 | 환자 및 관련 진료기록/X-Ray 영구 삭제 결과 |
| REQ-MDR-001 | POST | `/patients/{patient_id}/medical-records` | 진료기록 등록 | 사내 의료인 역할 | chart_number, symptoms, xray_image | 생성된 진료기록 정보 |
| REQ-MDR-002 | GET | `/patients/{patient_id}/medical-records` | 진료기록 목록 조회 | 로그인 된 사내 개발진/의료 실무진/연구진 | patient_id | record_id, chart_number, symptoms 요약, created_at |
| REQ-MDR-003 | GET | `/patients/{patient_id}/medical-records/{record_id}` | 진료기록 상세 조회 | 로그인 된 사내 개발진/의료 실무진/연구진 | patient_id, record_id | record_id, chart_number, symptoms, xray_image, created_at |

## 4. 요청/응답 설계 예시

### 4.1 환자 등록

**POST `/patients`**

Request Body 예시:

```json
{
  "name": "홍길동",
  "age": 55,
  "gender": "M",
  "phone_number": "010-1234-5678"
}
```

성공 응답 예시: `201 Created`

### 4.2 환자 목록 조회

**GET `/patients?search=홍&gender=M&min_age=40&max_age=70`**

- `search`: 이름 검색
- `gender`: 성별 필터
- `min_age`, `max_age`: 나이 범위 필터

성공 응답 예시: `200 OK`

### 4.3 환자 상세 조회

**GET `/patients/{patient_id}`**

- 존재하는 환자: `200 OK`
- 환자가 없음: `404 Not Found`

### 4.4 환자 정보 수정

**PATCH `/patients/{patient_id}`**

수정 가능 항목:
- name
- phone_number

성공 응답 예시: `200 OK`

### 4.5 환자 삭제

**DELETE `/patients/{patient_id}`**

삭제 시 확인 항목:
- 환자 정보
- 관련 진료기록
- 관련 X-Ray 이미지 파일

성공 응답 예시: `204 No Content` 또는 팀 공통 응답 형식에 맞춘 `200 OK`

> 실제 상태 코드는 기존 프로젝트의 응답 규칙과 맞춰 최종 결정한다.

### 4.6 진료기록 등록

**POST `/patients/{patient_id}/medical-records`**

입력 항목:
- 환자 고유 ID
- 진료 차트 번호
- 진료된 증상
- 흉부 X-Ray 이미지

X-Ray 이미지는 서버 실행 환경의 로컬 저장소에 저장한다.

성공 응답 예시: `201 Created`

### 4.7 진료기록 목록 조회

**GET `/patients/{patient_id}/medical-records`**

목록 필드:
- 진료 기록 ID
- 진료 차트 번호
- 증상: 100자 초과 시 생략 표시
- 생성일시

성공 응답 예시: `200 OK`

### 4.8 진료기록 상세 조회

**GET `/patients/{patient_id}/medical-records/{record_id}`**

상세 필드:
- 진료 기록 ID
- 차트 번호
- 증상
- 흉부 X-Ray 이미지
- 생성일시

성공 응답 예시: `200 OK`

## 5. 예외 처리 기준

- 인증되지 않은 사용자: `401 Unauthorized`
- 권한이 없는 사용자: `403 Forbidden`
- 환자 또는 진료기록이 존재하지 않음: `404 Not Found`
- 잘못된 입력값: 기존 프로젝트 Validation 규칙 사용
- 중복 또는 DB 관계 문제: 기존 모델/제약조건 확인 후 팀 공통 정책에 맞춰 처리

## 6. Swagger-UI 테스트 체크리스트

- 각 API 정상 응답 확인
- 존재하지 않는 patient_id / record_id 테스트
- 인증 없이 보호 API 호출 테스트
- 권한 조건이 있는 API의 허용/차단 테스트
- 환자 목록 검색/필터 테스트
- 환자 수정 시 허용되지 않은 필드가 변경되지 않는지 확인
- 환자 삭제 시 관련 진료기록/X-Ray가 함께 삭제되는지 확인
- X-Ray 업로드 및 저장 경로 확인
- 주요 API 응답 시간이 3초 이내인지 확인

## 7. Git 작업 흐름

1. 최신 기준 브랜치 확인
2. 담당 기능 브랜치 생성
3. 담당 API 구현
4. Swagger-UI 테스트
5. `git diff --check`
6. `git status`
7. Commit
8. Push
9. Pull Request 생성
10. 팀 검토 후 `main` 또는 `develop`에 병합

## 8. 역할 분담안

| 담당자 | 요구사항 | 담당 기능 |
|---|---|---|
| 안애영 | REQ-MDR-001 | 진료기록 등록 + X-Ray 업로드/저장 + 공통 통합 |
| 한성규 | REQ-PTNT-003, REQ-MDR-003 | 환자 상세 조회 + 진료기록 상세 조회 |
| 김태호 | REQ-PTNT-002 | 환자 목록 조회 + 검색/필터 |
| 배수빈 | REQ-PTNT-001, REQ-PTNT-004 | 환자 등록 + 환자 정보 수정 |
| 김효민 | REQ-PTNT-005, REQ-MDR-002 | 환자 삭제 + 진료기록 목록 조회 |

## 9. 제출 전 확인

- 모든 팀원이 최소 1개의 API를 작성했는지 확인
- Swagger-UI 테스트 결과 확인
- PR 및 Merge 상태 확인
- `docs/5일차_환자관리_API_설계.md`가 최종 브랜치에 포함되었는지 확인
- 민감 정보가 Commit되지 않았는지 확인
