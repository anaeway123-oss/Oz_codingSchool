# 4일차 User API 설계

## 1. 개요

본 문서는 User 사용자 요구사항 정의서를 기준으로
회원가입, 로그인, 인증/인가, 로그아웃, 회원 관리, 마이페이지 기능에 필요한
User API를 설계한 문서입니다.

---

## 2. API 목록

| 요구사항 ID | 기능 | Method | Endpoint | 인증 |
|---|---|---|---|---|
| REQ-USER-001 | 회원가입 | POST | `/users/signup` | 불필요 |
| REQ-USER-002 | 로그인 | POST | `/auth/login` | 불필요 |
| NFR-USER-001 | Access Token 재발급 | POST | `/auth/refresh` | Refresh Token 필요 |
| REQ-USER-003 | 로그아웃 | POST | `/auth/logout` | 필요 |
| REQ-USER-004 | 회원 목록 조회 | GET | `/users` | Admin |
| REQ-USER-005 | 회원 권한 변경 | PATCH | `/users/{user_id}/role` | Admin |
| REQ-USER-006 | 마이페이지 조회 | GET | `/users/me` | 필요 |
| REQ-USER-007 | 회원 정보 수정 | PATCH | `/users/me` | 필요 |
| REQ-USER-008 | 비밀번호 변경 | PATCH | `/users/me/password` | 필요 |
| REQ-USER-009 | 회원 탈퇴 | DELETE | `/users/me` | 필요 |

---

## 3. 회원가입 API

### POST `/users/signup`

새로운 사용자를 등록합니다.

### Request Body

- email: 이메일
- password: 비밀번호
- name: 이름
- department: 부서 (연구 / 의료 / 개발)
- gender: 성별 (M / F)
- phone_number: 휴대폰 번호

### 처리 내용

1. 회원가입에 필요한 입력값을 전달받습니다.
2. 입력값을 검증합니다.
3. 비밀번호는 안전하게 처리하여 Database에 저장합니다.
4. 신규 사용자 정보를 Database에 저장합니다.
5. 신규 사용자의 기본 권한은 `PENDING`(대기자)으로 설정합니다.

### Response

- `201 Created`: 회원가입 성공
- `400 Bad Request`: 잘못된 입력값
- `409 Conflict`: 중복된 사용자 정보가 존재하는 경우

---

## 4. 로그인 API

### POST `/auth/login`

회원가입을 완료한 사용자가 이메일과 비밀번호를 입력하여 로그인합니다.

### Request Body

- email: 이메일
- password: 비밀번호

### 처리 내용

1. 이메일에 해당하는 사용자를 조회합니다.
2. 입력한 비밀번호가 저장된 사용자 정보와 일치하는지 검증합니다.
3. 로그인에 성공하면 Access Token과 Refresh Token을 발급합니다.
4. Refresh Token은 클라이언트에서 직접 접근할 수 없도록 httpOnly 쿠키로 전달합니다.

### Response

- `200 OK`: 로그인 성공
- `401 Unauthorized`: 로그인 정보가 올바르지 않은 경우

---

## 5. JWT 인증 / 인가

JWT(JSON Web Token)를 사용하여 로그인한 사용자를 인증하고
API 접근 권한을 확인합니다.

### Access Token

- 만료 주기: 30분
- 로그인 이후 API 인가에 사용합니다.
- JWT Payload에는 최소 식별 정보인 `user_id`만 저장합니다.

### Refresh Token

- 만료 주기: 7일
- Access Token이 만료된 경우 새로운 Access Token을 발급받기 위해 사용합니다.
- 클라이언트에서 직접 접근할 수 없도록 httpOnly 쿠키로 전달합니다.
- Refresh Token까지 만료된 경우 다시 로그인을 진행하도록 합니다.

### POST `/auth/refresh`

유효한 Refresh Token을 이용하여 새로운 Access Token을 발급합니다.

### Response

- `200 OK`: Access Token 재발급 성공
- `401 Unauthorized`: Refresh Token이 없거나 유효하지 않은 경우

---

## 6. 로그아웃 API

### POST `/auth/logout`

로그인한 사용자가 로그아웃을 진행합니다.

### 처리 내용

1. 로그인 상태를 종료하기 위한 처리를 수행합니다.
2. Refresh Token이 전달된 httpOnly 쿠키를 제거합니다.
3. 로그아웃 성공 후 클라이언트에서는 로그인 페이지로 이동합니다.

### Response

- `200 OK`: 로그아웃 성공
- `401 Unauthorized`: 인증되지 않은 사용자

---

## 7. 회원 목록 조회 API

### GET `/users`

Admin 권한의 사용자가 전체 회원 목록을 조회합니다.

### Query Parameter

- email: 이메일 검색
- name: 이름 검색
- department: 부서별 필터

### 조회 항목

- id: 고유 ID
- email: 이메일
- name: 이름
- department: 부서 (연구 / 의료 / 개발)
- gender: 성별 (M / F)
- phone_number: 휴대폰 번호
- is_active: 계정 활성화 여부

### 처리 내용

1. 요청한 사용자가 Admin 권한인지 확인합니다.
2. 전체 회원 목록을 조회합니다.
3. 이메일 또는 이름을 이용한 검색을 지원합니다.
4. 부서별 필터 조회를 지원합니다.

### Response

- `200 OK`: 회원 목록 조회 성공
- `401 Unauthorized`: 인증되지 않은 사용자
- `403 Forbidden`: Admin 권한이 없는 사용자

---

## 8. 회원 권한 변경 API

### PATCH `/users/{user_id}/role`

Admin 권한의 사용자가 선택한 회원의 권한을 변경합니다.

### 변경 가능한 권한

- 대기자
- 스태프
- 어드민

### Request Body

- role: 변경할 권한

### 처리 내용

1. 요청한 사용자가 Admin 권한인지 확인합니다.
2. 권한을 변경할 대상 사용자를 확인합니다.
3. 선택한 권한으로 변경합니다.

### Response

- `200 OK`: 회원 권한 변경 성공
- `400 Bad Request`: 잘못된 권한 값
- `401 Unauthorized`: 인증되지 않은 사용자
- `403 Forbidden`: Admin 권한이 없는 사용자
- `404 Not Found`: 대상 사용자를 찾을 수 없는 경우

---

## 9. 마이페이지 조회 API

### GET `/users/me`

로그인한 사용자가 마이페이지에서 본인의 정보를 조회합니다.

### 조회 항목

- name: 이름
- email: 이메일
- department: 부서 (연구 / 의료 / 개발)
- gender: 성별 (M / F)
- phone_number: 휴대폰 번호
- role: 권한 (대기자 / 스태프 / 어드민)

### Response

- `200 OK`: 마이페이지 조회 성공
- `401 Unauthorized`: 인증되지 않은 사용자

---

## 10. 회원 정보 수정 API

### PATCH `/users/me`

로그인한 사용자가 마이페이지에서 본인의 정보를 수정합니다.

회원 정보 수정은 Partial Update 방식으로 처리합니다.

### 수정 가능한 항목

- department: 부서
- phone_number: 휴대폰 번호

### 처리 내용

1. 로그인한 사용자의 정보를 확인합니다.
2. 요청에 포함된 수정 가능한 항목을 확인합니다.
3. 전달된 항목만 부분적으로 수정합니다.
4. 수정된 정보를 Database에 반영합니다.

### Response

- `200 OK`: 회원 정보 수정 성공
- `400 Bad Request`: 잘못된 입력값
- `401 Unauthorized`: 인증되지 않은 사용자

---

## 11. 비밀번호 변경 API

### PATCH `/users/me/password`

로그인한 사용자가 마이페이지에서 자신의 비밀번호를 변경합니다.

### Request Body

- current_password: 기존 비밀번호
- new_password: 새로운 비밀번호

### 처리 내용

1. 사용자가 입력한 기존 비밀번호가 일치하는지 검증합니다.
2. 기존 비밀번호가 일치하면 새로운 비밀번호를 안전하게 처리합니다.
3. 새로운 비밀번호를 Database에 반영합니다.

### Response

- `200 OK`: 비밀번호 변경 성공
- `400 Bad Request`: 기존 비밀번호가 일치하지 않거나 입력값이 올바르지 않은 경우
- `401 Unauthorized`: 인증되지 않은 사용자

---

## 12. 회원 탈퇴 API

### DELETE `/users/me`

로그인한 사용자가 마이페이지에서 회원 탈퇴를 진행합니다.

### 처리 내용

1. 로그인한 본인 사용자를 확인합니다.
2. 회원과 관련된 정보를 Database에서 즉시 삭제합니다.

### Response

- `204 No Content`: 회원 탈퇴 성공
- `401 Unauthorized`: 인증되지 않은 사용자

---

## 13. 비밀번호 입력 보안

NFR-USER-002 요구사항에 따라 모든 비밀번호 입력 화면에서는
비밀번호 입력 내용을 기본적으로 마스킹 처리합니다.

사용자는 비밀번호 보기 기능을 통해 입력한 비밀번호를 확인할 수 있습니다.

비밀번호 마스킹 및 보기/숨김 기능은 클라이언트 화면에서 처리하며,
서버 API는 사용자의 비밀번호 원문을 응답으로 반환하지 않습니다.

---

## 14. API 성능

NFR-USER-003 요구사항에 따라 모든 User API는
최대 3초 이내에 로직을 처리하고 응답할 수 있도록 구현합니다.

---

## 15. 전체 API 흐름

### 회원가입 및 인증 흐름

회원가입
→ 로그인
→ Access Token / Refresh Token 발급
→ Access Token을 이용하여 인증이 필요한 API 사용
→ Access Token 만료 시 Refresh Token을 이용하여 Access Token 재발급
→ Refresh Token까지 만료된 경우 재로그인
→ 로그아웃

### 일반 사용자 기능

로그인
→ 마이페이지 조회
→ 회원 정보 수정
→ 비밀번호 변경
→ 회원 탈퇴

### 관리자 기능

Admin 로그인
→ 회원 목록 조회
→ 이메일 / 이름 검색
→ 부서별 필터 조회
→ 회원 선택
→ 회원 권한 변경
