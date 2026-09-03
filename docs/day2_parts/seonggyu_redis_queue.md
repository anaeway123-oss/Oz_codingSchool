# 성규 - Redis · Queue 학습 정리

## 1. Redis의 역할

### Redis란?

Redis는 메모리를 중심으로 데이터를 빠르게 저장하고 조회할 수 있는 데이터 저장소입니다.

일반적인 관계형 데이터베이스처럼 데이터를 영구 보관하는 용도로만 사용하는 것이 아니라,
캐시, 세션 저장소, 메시지 전달, 작업 대기열(Queue) 등 다양한 용도로 활용할 수 있습니다.

### 왜 이번 구조에서 Redis가 필요한가?

우리 프로젝트에서는 사용자가 업로드한 X-ray 이미지를 AI가 분석하는 과정이 일반 API 요청보다 오래 걸릴 수 있습니다.

FastAPI가 이미지 분석이 끝날 때까지 모든 작업을 직접 처리하도록 만들면 요청이 몰릴 경우
응답 시간이 길어지고 동시에 처리해야 할 작업이 증가할 수 있습니다.

이때 Redis를 FastAPI와 AI Worker 사이의 작업 대기 공간으로 두면,
FastAPI는 분석 요청을 Queue에 등록하고 AI Worker가 순서대로 가져가 처리할 수 있습니다.

즉 Redis는 이번 구조에서 다음 역할을 합니다.

- FastAPI와 AI Worker 사이의 중간 연결 역할
- 처리해야 할 AI 분석 작업을 임시로 보관
- 요청이 한꺼번에 들어와도 작업을 Queue에 쌓아 순차적으로 전달
- 웹 요청 처리와 AI 추론 작업을 서로 분리

---

## 2. Queue(작업 대기열)의 개념과 필요한 이유

### Queue란?

Queue는 처리해야 할 작업을 잠시 저장해 두는 대기열입니다.

쉽게 생각하면 병원의 접수 대기표와 비슷합니다.

환자가 한꺼번에 접수하더라도 의사가 모든 환자를 동시에 진료하는 것이 아니라
대기 순서에 따라 한 명씩 또는 처리 가능한 수만큼 진료합니다.

소프트웨어에서도 비슷하게 동작합니다.

1. 처리할 작업이 들어옵니다.
2. 작업을 Queue에 저장합니다.
3. Worker가 Queue에서 작업을 가져옵니다.
4. 작업을 처리합니다.
5. 다음 작업을 가져옵니다.

### Queue가 필요한 이유

AI 이미지 분석과 같이 시간이 오래 걸리는 작업이 동시에 많이 들어오면
FastAPI 서버가 모든 작업을 직접 처리하기에는 부담이 커질 수 있습니다.

Queue를 사용하면 요청을 바로 처리하려고 경쟁시키는 대신
처리할 작업을 대기열에 저장해 둘 수 있습니다.

따라서 다음과 같은 장점이 있습니다.

- 갑자기 요청이 증가해도 작업을 대기시킬 수 있음
- FastAPI가 AI 추론을 직접 수행하지 않아 역할을 분리할 수 있음
- Worker가 처리 가능한 만큼 작업을 가져갈 수 있음
- Worker를 여러 개 운영할 경우 작업을 나누어 처리할 수 있음
- 웹 요청 처리와 오래 걸리는 AI 작업의 결합도를 낮출 수 있음

Queue 자체가 모든 동시성 문제를 자동으로 해결하는 것은 아니지만,
작업을 어떤 순서와 속도로 처리할지 관리하기 쉬운 구조를 만드는 데 도움이 됩니다.

---

## 3. Producer → Redis Queue → Consumer 흐름

이번 프로젝트의 기본 흐름은 다음과 같습니다.

`Producer → Redis Queue → Consumer`

### Producer

Producer는 처리해야 할 작업을 만들어 Queue에 넣는 역할입니다.

우리 프로젝트에서는 FastAPI가 Producer 역할을 합니다.

사용자가 X-ray 분석을 요청하면 FastAPI는
AI 분석에 필요한 작업 정보를 만들어 Redis Queue에 등록합니다.

### Redis Queue

Redis Queue는 Producer가 등록한 작업을 임시로 보관합니다.

AI Worker가 바로 처리할 수 없는 경우에도 작업은 Queue에서 대기할 수 있습니다.

예를 들어 동시에 10개의 AI 분석 요청이 들어왔는데
Worker가 한 번에 2개만 처리할 수 있다면,
나머지 작업은 Queue에서 자신의 처리 순서를 기다릴 수 있습니다.

### Consumer

Consumer는 Queue에서 작업을 꺼내 실제 처리를 담당합니다.

우리 프로젝트에서는 AI Worker가 Consumer 역할을 합니다.

AI Worker는 Redis Queue에서 분석 요청을 가져온 뒤
X-ray 이미지에 대한 폐렴 예측을 수행하고 결과를 저장합니다.

### 전체 흐름

`사용자 → FastAPI → Redis Queue → AI Worker → AI 분석 → 결과 저장`

쉽게 정리하면 다음과 같습니다.

- 사용자: X-ray 분석 요청
- FastAPI: 요청 접수 및 작업 생성
- Redis Queue: 작업 대기
- AI Worker: 작업 가져오기
- AI 모델: 폐렴 여부 예측
- 결과 저장소: 예측 결과 저장
- 사용자: 저장된 결과 확인

---

## 4. 우리 프로젝트에서의 적용

우리 프로젝트는 X-ray 이미지를 이용해 폐렴 여부를 예측하는 AI 웹 서비스입니다.

기존처럼 FastAPI가 요청 접수부터 AI 분석까지 모두 담당하면
AI 분석 시간이 길어질수록 API 응답도 영향을 받을 수 있습니다.

Event-Driven Architecture에서는 역할을 다음과 같이 분리할 수 있습니다.

### FastAPI의 역할

- 사용자 요청 수신
- 입력값 및 이미지 정보 확인
- AI 분석 작업 생성
- Redis Queue에 작업 등록
- 작업 접수 상태 또는 결과 조회 API 제공

### Redis Queue의 역할

- AI 분석 요청을 대기열에 저장
- FastAPI와 AI Worker 사이에서 작업 전달
- Worker가 처리할 수 있을 때까지 작업 보관

### AI Worker의 역할

- Redis Queue에서 작업 가져오기
- X-ray 이미지 로드
- AI 모델 추론 실행
- 폐렴 예측 결과 생성
- 결과 저장

이 구조를 사용하면 FastAPI는 웹 요청 처리에 집중하고,
AI Worker는 시간이 오래 걸릴 수 있는 AI 추론에 집중할 수 있습니다.

---

## 5. Excalidraw 아키텍처 설계 시 포함할 요소

아키텍처 설계도에는 다음 흐름이 명확하게 보여야 합니다.

`사용자 → FastAPI → Redis Queue → AI Worker → 결과 저장`

### 사용자

- X-ray 이미지 업로드
- AI 분석 요청
- 분석 결과 조회

### FastAPI

**Producer 역할**

- 요청 접수
- 작업 생성
- Redis Queue에 작업 등록
- 결과 조회 요청 처리

### Redis Queue

**작업 대기열**

- AI 분석 작업 저장
- 대기 중인 작업 관리
- AI Worker에 작업 전달

### AI Worker

**Consumer 역할**

- Queue에서 작업 가져오기
- AI 모델 실행
- 폐렴 여부 및 confidence 생성

### 결과 저장

- AI 분석 결과 저장
- FastAPI가 저장된 결과를 조회
- 사용자에게 결과 제공

### 도식에서 강조할 부분

FastAPI와 AI Worker를 서로 다른 영역으로 표현하여 역할 분리를 명확하게 보여줍니다.

FastAPI는 웹 요청 처리와 작업 등록을 담당하고,
AI Worker는 실제 AI 연산을 담당하도록 표현합니다.

Redis Queue는 두 영역 사이에 위치시켜
FastAPI와 AI Worker를 연결하는 작업 대기열이라는 점을 보여줍니다.

---

## 6. 참고 자료

- Redis 공식 문서 - Redis Lists
- Redis 공식 문서 - Redis Streams
- Redis 공식 문서 - Redis Streaming
- Docker 웹 서비스 배포 2일차 팀 작업 가이드
