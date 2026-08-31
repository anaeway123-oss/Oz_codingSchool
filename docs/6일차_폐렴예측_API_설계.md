# 6일차 폐렴 예측 API 설계

## 1. 개요 및 목적
* 진료기록(Medical Record)에 등록된 흉부 X-ray 이미지를 AI 모델(SimpleCNN)로 분석하여 폐렴 예측 결과를 반환합니다.
* 동일한 기록과 모델에 대한 예측 결과가 DB에 이미 존재할 경우, AI를 재실행하지 않고 기존 결과를 반환하여 중복 저장을 방지합니다.

## 2. 기본 정보
* **HTTP Method:** `POST`
* **URL:** `/patients/{patient_id}/medical-records/{record_id}/ai-predictions`
* **인증 (Authentication):** JWT Bearer Token 필수
* **권한 (Authorization):** 의료팀, 개발팀, 연구팀, 관리자(ADMIN) 전체 접근 가능

## 3. 요청 데이터 (Request)
* **Path Parameters:**
  * `patient_id` (int, 필수): 환자 식별자 ID
  * `record_id` (int, 필수): 진료기록 식별자 ID
* **Request Body (JSON, 선택):**
```json
{
  "ai_model": "SimpleCNN"
}