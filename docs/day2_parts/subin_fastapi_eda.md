# 수빈 - FastAPI · Event-Driven Architecture 학습 정리

## 1. 동시성 문제와 Event-Driven Architecture

### 무엇인가?

동시성은 여러 사용자의 요청이 같은 시간대에 겹쳐서 처리되는 상황을 의미합니다. 웹 서비스에서는 여러 사용자가 동시에 API를 호출할 수 있으므로 자연스럽게 발생합니다.

동시 요청이 많아지면 처리 시간이 긴 작업 때문에 다른 요청까지 오래 기다리거나, 같은 데이터를 동시에 수정해 결과가 중복되는 문제가 생길 수 있습니다. 예를 들어 여러 사용자가 같은 진료기록의 폐렴 예측을 동시에 요청하면 동일한 예측 작업이 중복 실행될 수 있습니다.

Event-Driven Architecture(이벤트 기반 아키텍처)는 “어떤 일이 발생했다”는 이벤트를 중심으로 시스템을 나누는 구조입니다. 일반적으로 다음 세 역할로 구성됩니다.

- Producer(생산자): 이벤트나 작업을 만들어 보내는 역할
- Event Channel 또는 Queue(전달 통로·대기열): 작업을 임시로 보관하고 전달하는 역할
- Consumer(소비자): 전달받은 작업을 실제로 처리하는 역할

### 왜 필요한가?

폐렴 예측처럼 시간이 오래 걸릴 수 있는 AI 작업을 FastAPI가 요청 안에서 직접 모두 처리하면, 예측이 끝날 때까지 응답이 지연됩니다. 요청이 한꺼번에 몰리면 서버의 부담이 커지고 일부 요청은 시간 초과나 실패로 이어질 수 있습니다.

이벤트 기반 구조에서는 FastAPI와 AI Worker의 역할을 분리합니다. FastAPI는 요청을 빠르게 접수하고 작업을 Queue에 전달하며, AI Worker는 Queue에서 작업을 하나씩 가져와 처리합니다. 이를 통해 다음과 같은 장점이 생깁니다.

- FastAPI가 AI 예측 완료까지 계속 기다리지 않아도 됩니다.
- 여러 요청이 들어와도 Queue에 순서대로 보관할 수 있습니다.
- AI Worker의 수를 늘려 작업 처리량을 조절할 수 있습니다.
- API 서버와 AI 처리 기능을 서로 독립적으로 관리할 수 있습니다.

### 우리 프로젝트에서는 어디에 쓰는가?

우리 프로젝트에서는 사용자가 흉부 X-ray 폐렴 예측을 요청했을 때 활용할 수 있습니다.

FastAPI는 환자 ID, 진료기록 ID, X-ray 이미지 경로 등의 작업 정보를 Redis Queue에 전달합니다. AI Worker는 해당 작업을 가져와 X-ray 이미지를 모델에 입력하고, 폐렴 여부와 신뢰도(Confidence)를 계산합니다. 예측 결과는 데이터베이스에 저장한 뒤 사용자가 결과 조회 API를 통해 확인하도록 구성할 수 있습니다.

### 쉬운 예시

병원 접수창구를 생각하면 이해하기 쉽습니다.

- FastAPI는 환자의 검사 요청을 접수하는 직원입니다.
- Redis Queue는 접수된 검사표가 순서대로 놓이는 대기함입니다.
- AI Worker는 검사표를 가져가 실제로 X-ray를 분석하는 검사 담당자입니다.
- 데이터베이스는 검사 결과를 보관하는 진료 시스템입니다.

접수 직원이 직접 X-ray 분석까지 하면 다음 환자를 받을 수 없습니다. 접수와 검사를 분리하면 접수 직원은 다음 요청을 계속 받을 수 있고, 검사 담당자는 대기함에 들어온 작업을 차례로 처리할 수 있습니다.

## 2. FastAPI의 역할과 Producer 개념

### 무엇인가?

FastAPI는 사용자의 HTTP 요청을 받아 필요한 데이터를 확인하고, 적절한 응답을 돌려주는 웹 API 서버입니다.

Producer는 처리해야 할 이벤트나 작업을 만들어 Queue에 보내는 역할입니다. 우리 프로젝트에서는 FastAPI가 폐렴 예측 작업을 생성하여 Redis Queue에 전달하므로 Producer에 해당합니다.

FastAPI가 담당하는 주요 역할은 다음과 같습니다.

- 사용자의 폐렴 예측 요청 접수
- 로그인 여부와 사용 권한 확인
- 환자 및 진료기록 정보 확인
- 요청 데이터의 형식과 필수값 검증
- AI Worker가 처리할 작업 정보 생성
- 생성한 작업을 Redis Queue에 전달
- 작업 접수 결과를 사용자에게 응답

### 왜 필요한가?

FastAPI가 요청 접수부터 AI 예측까지 모두 직접 처리하면, 예측이 끝날 때까지 요청을 계속 붙잡고 있어야 합니다. 반면 FastAPI를 Producer로 사용하면 예측 작업을 Redis Queue에 전달한 뒤 다른 요청을 처리할 수 있습니다.

이 구조에서는 FastAPI와 AI Worker의 책임도 명확하게 나뉩니다.

- FastAPI: 요청 접수, 인증, 입력 검증, 작업 생성 및 전달
- AI Worker: X-ray 이미지 전처리, 모델 추론 및 결과 저장

역할을 분리하면 API 요청 처리와 AI 연산을 각각 독립적으로 관리하고 확장하기 쉬워집니다.

### 우리 프로젝트에서는 어디에 쓰는가?

사용자가 특정 환자의 진료기록에 대해 폐렴 예측을 요청하면 FastAPI는 다음과 같은 작업 정보를 생성할 수 있습니다.

```json
{
  "job_id": "prediction-123",
  "patient_id": 1,
  "record_id": 10,
  "xray_image_path": "/media/xray/example.png"
}
```
이 데이터는 실제 예측 결과가 아니라 AI Worker에게 전달하는 작업 지시서입니다. FastAPI는 이 작업을 Redis Queue에 넣고, 사용자에게 작업이 접수되었다는 응답을 보냅니다.
작업을 비동기로 접수하는 API라면 202 Accepted 상태 코드와 작업 ID를 응답하는 방식을 사용할 수 있습니다. 단, 실제 응답 코드와 필드 이름은 팀의 최종 API 명세에 맞춰 결정해야 합니다.
```json
{
  "message": "폐렴 예측 작업이 접수되었습니다.",
  "job_id": "prediction-123",
  "status": "queued"
}
```

### 쉬운 예시
FastAPI는 택배 접수 직원과 비슷합니다.
접수 직원은 택배 내용과 주소가 올바른지 확인하고 운송장 번호를 만든 뒤, 택배를 배송 대기 장소에 놓습니다. 접수 직원이 직접 배송까지 담당하지 않는 것처럼 FastAPI도 AI 예측을 직접 수행하지 않고, 작업 정보를 만들어 Redis Queue에 전달합니다.

## 3. FastAPI → Redis Queue 작업 전달 흐름

### 전체 흐름

FastAPI가 Redis Queue로 폐렴 예측 작업을 전달하는 흐름은 다음과 같습니다.

1. 사용자가 폐렴 예측 API를 호출합니다.
2. FastAPI가 로그인 여부와 사용 권한을 확인합니다.
3. 환자, 진료기록 및 X-ray 이미지가 존재하는지 확인합니다.
4. FastAPI가 AI Worker에게 전달할 작업 데이터를 생성합니다.
5. 작업 데이터를 JSON처럼 전달 가능한 형식으로 변환합니다.
6. FastAPI가 작업을 Redis Queue에 추가합니다.
7. AI Worker가 Queue에서 대기 중인 작업을 가져갑니다.
8. AI Worker가 X-ray 이미지를 불러와 전처리하고 폐렴 예측을 실행합니다.
9. AI Worker가 폐렴 여부와 Confidence 등의 결과를 데이터베이스에 저장합니다.
10. 사용자는 결과 조회 API를 호출해 저장된 예측 결과를 확인합니다.

흐름을 한 줄로 표현하면 다음과 같습니다.

```text
사용자 요청
→ FastAPI
→ 요청 검증 및 작업 생성
→ Redis Queue
→ AI Worker
→ X-ray 전처리 및 모델 추론
→ 결과 DB 저장
→ 결과 조회
```

### Redis Queue에는 무엇을 전달하는가?
Queue에는 X-ray 이미지 자체를 직접 넣기보다, Worker가 작업을 처리하는 데 필요한 최소한의 정보를 전달하는 것이 좋습니다.
예시는 다음과 같습니다.

```json
{
  "job_id": "prediction-123",
  "patient_id": 1,
  "record_id": 10,
  "xray_image_path": "/media/xray/example.png",
  "ai_model": "SimpleCNN"
}
```

각 값의 의미는 다음과 같습니다.
- job_id: 작업을 구분하기 위한 고유 번호
- patient_id: 예측 대상 환자 번호
- record_id: 예측과 연결된 진료기록 번호
- xray_image_path: Worker가 불러올 X-ray 이미지 경로
- ai_model: 예측에 사용할 모델 이름
실제 필드명과 저장 방식은 팀의 최종 설계에 따라 달라질 수 있습니다.
### Redis Queue는 어떻게 동작하는가?

Redis의 List 자료구조는 작업을 순서대로 저장하는 Queue로 사용할 수 있습니다. Producer인 FastAPI가 작업을 넣고, Consumer인 AI Worker가 작업을 꺼내 처리합니다.

예를 들어 다음과 같은 방식을 사용할 수 있습니다.

```text
FastAPI: LPUSH로 작업 추가
AI Worker: BRPOP으로 작업 대기 및 가져오기
```

BRPOP은 Queue가 비어 있으면 새 작업이 들어올 때까지 기다렸다가 작업을 가져올 수 있습니다. 다만 실제 명령과 라이브러리는 팀에서 선택한 구현 방식에 맞춰 결정해야 합니다.
### 오류가 발생하면 어떻게 하는가?

Queue를 사용하더라도 다음 상황에 대한 처리가 필요합니다.
- 잘못된 환자 또는 진료기록 요청은 Queue에 넣기 전에 거절합니다.
- X-ray 이미지가 없으면 작업을 생성하지 않습니다.
- 같은 진료기록의 동일한 예측 작업이 중복 등록되지 않도록 확인합니다.
- Worker 처리 실패 시 작업 상태와 오류 내용을 기록합니다.
- 필요한 경우 실패한 작업의 재시도 횟수를 제한합니다.
이러한 처리를 통해 작업이 사라지거나 무한히 반복되는 문제를 줄일 수 있습니다.
### 쉬운 예시

음식점 주문 과정을 생각하면 이해하기 쉽습니다.
- 손님은 사용자입니다.
- 주문을 받는 직원은 FastAPI입니다.
- 주문표 대기판은 Redis Queue입니다.
- 음식을 만드는 요리사는 AI Worker입니다.
- 완성된 음식 정보는 데이터베이스에 저장되는 예측 결과입니다.
주문을 받은 직원은 주문표를 대기판에 붙이고 다음 손님의 주문을 받습니다. 요리사는 대기판에서 주문표를 하나씩 가져와 처리합니다. 따라서 주문이 몰려도 접수와 조리 작업을 분리하여 관리할 수 있습니다.

## 4. 우리 프로젝트에서의 적용

### 실제 API 경로

우리 프로젝트의 폐렴 예측 API 경로는 다음과 같습니다.

```text
POST /patients/{patient_id}/medical-records/{record_id}/ai-predictions
GET  /patients/{patient_id}/medical-records/{record_id}/ai-predictions
```

현재 경로를 유지하면서 POST 요청의 처리 방식을 Event-Driven Architecture로 분리할 수 있습니다.

### 구성 요소별 역할

#### FastAPI — Producer

FastAPI는 사용자 요청을 가장 먼저 받는 Producer 역할을 담당합니다.

- 로그인 및 사용 권한 확인
- `patient_id`와 `record_id` 확인
- 진료기록과 X-ray 이미지 존재 여부 확인
- 중복 예측 요청 여부 확인
- AI 예측 작업 데이터 생성
- 생성한 작업을 Redis Queue에 전달
- 작업 접수 결과와 작업 ID 응답

FastAPI는 요청 접수와 작업 전달에 집중하며, 시간이 오래 걸리는 모델 추론은 직접 수행하지 않습니다.

#### Redis Queue — 작업 대기열

Redis Queue는 FastAPI가 만든 작업을 AI Worker가 가져갈 때까지 보관합니다. 요청이 한꺼번에 들어와도 작업을 대기열에 쌓아 순서대로 처리할 수 있도록 연결합니다.

#### AI Worker — Consumer

AI Worker는 Redis Queue에서 작업을 가져와 실제 폐렴 예측을 수행합니다.

- 작업 데이터에서 진료기록과 X-ray 경로 확인
- X-ray 이미지 불러오기 및 전처리
- AI 모델 추론
- 폐렴 여부와 Confidence 계산
- 예측 결과 또는 실패 정보 저장

#### 데이터베이스 — 상태 및 결과 저장

데이터베이스에는 작업 상태와 예측 결과를 저장할 수 있습니다.

```text
queued → processing → completed
                    ↘ failed
```

- `queued`: 작업이 Queue에서 대기 중
- `processing`: AI Worker가 예측을 수행 중
- `completed`: 예측 완료 및 결과 저장 성공
- `failed`: 이미지 또는 모델 처리 중 오류 발생

상태값의 정확한 이름과 저장 위치는 팀의 최종 설계에서 결정해야 합니다.

### 프로젝트 요청 처리 예시

1. 사용자가 POST 예측 API를 호출합니다.
2. FastAPI가 요청을 검증하고 작업 ID를 생성합니다.
3. FastAPI가 작업 정보를 Redis Queue에 전달합니다.
4. 사용자에게 작업 접수 결과를 먼저 응답합니다.
5. AI Worker가 Queue에서 작업을 가져와 예측합니다.
6. AI Worker가 폐렴 여부와 Confidence를 데이터베이스에 저장합니다.
7. 사용자가 GET API를 호출해 저장된 결과를 확인합니다.

비동기 작업 접수 응답에는 다음 형식을 고려할 수 있습니다.

```json
{
  "job_id": "prediction-123",
  "status": "queued",
  "message": "폐렴 예측 작업이 접수되었습니다."
}
```

비동기로 작업만 접수한 경우에는 `202 Accepted`를 사용할 수 있지만, 실제 상태 코드와 응답 필드는 팀의 최종 API 명세에 맞춰 결정해야 합니다.

### 동시 요청 처리 시 확인할 점

같은 진료기록에 대해 여러 사용자가 동시에 예측을 요청할 수 있으므로 다음 사항을 고려해야 합니다.

- 같은 `record_id`와 같은 AI 모델의 작업이 이미 처리 중인지 확인
- 동일한 작업의 중복 Queue 등록 방지
- 작업마다 고유한 `job_id` 부여
- Worker 실패 시 상태를 `failed`로 기록
- 재시도 횟수와 실패 처리 기준 설정
- 완료된 작업과 실패한 작업의 보관 기간 설정

### 쉬운 예시

사용자가 폐렴 예측 버튼을 누르면 FastAPI는 “예측 요청을 접수했습니다”라고 알려주고 작업표를 Redis Queue에 넣습니다. AI Worker는 대기 중인 작업표를 가져가 X-ray를 분석합니다.

분석이 끝나면 결과를 데이터베이스에 저장하고, 사용자는 결과 조회 API를 통해 폐렴 여부와 Confidence를 확인할 수 있습니다. 이렇게 구성하면 여러 사용자가 동시에 예측을 요청하더라도 FastAPI가 모든 AI 연산을 직접 처리하지 않아도 됩니다.


## 5. 참고 자료

### 핵심 참고 자료

- [FastAPI 공식 문서 - 동시성과 async / await](https://fastapi.tiangolo.com/ko/async/)
- [FastAPI 공식 문서 - 자습서·사용자 안내서](https://fastapi.tiangolo.com/ko/tutorial/)
- [FastAPI 공식 문서 - 요청 본문](https://fastapi.tiangolo.com/ko/tutorial/body/)
- [FastAPI 공식 문서 - 응답 상태 코드](https://fastapi.tiangolo.com/ko/tutorial/response-status-code/)
- [Redis 공식 문서 - Redis Lists](https://redis.io/docs/latest/develop/data-types/lists/)
- [Redis 공식 문서 - Redis Job Queue](https://redis.io/docs/latest/develop/use-cases/job-queue/)
- [Microsoft Learn - Event-Driven Architecture Style](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven)

### 보조 참고 자료

- [FastAPI 공식 문서 - 폼 및 파일 요청](https://fastapi.tiangolo.com/ko/tutorial/request-forms-and-files/)
- OZ 코딩스쿨 Docker 웹 서비스 배포 2일차 수업 자료
