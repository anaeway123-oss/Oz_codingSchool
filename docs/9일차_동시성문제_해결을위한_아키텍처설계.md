# 9일차 동시성 문제 해결을 위한 아키텍처 설계

## 1. 과제 개요

FastAPI + Redis 기반 Event-Driven Architecture를 학습하고,
동시성 문제를 해결하기 위한 아키텍처를 설계합니다.

---

## 2. 기존 동기 처리 방식과 동시성 문제

<!-- 담당: 수빈 -->
<!-- 수빈님의 docs/day2_parts/subin_fastapi_eda.md 내용을 최종 통합 단계에서 반영 -->

---

## 3. Event-Driven Architecture

<!-- 담당: 수빈 -->
<!-- Event-Driven Architecture의 개념과 필요한 이유 정리 -->

---

## 4. FastAPI의 역할

<!-- 담당: 수빈 -->
<!-- FastAPI의 역할과 Redis Queue로 작업을 전달하는 흐름 정리 -->

---

## 5. Redis와 작업 Queue

<!-- 담당: 성규 -->
<!-- 성규님의 docs/day2_parts/seonggyu_redis_queue.md 내용을 최종 통합 단계에서 반영 -->

---

## 6. AI Worker의 역할

<!-- 담당: 효민 -->
<!-- 효민님의 docs/day2_parts/hyomin_ai_worker.md 내용을 최종 통합 단계에서 반영 -->

---

## 7. FastAPI와 AI Worker를 분리하는 이유

<!-- 담당: 효민 -->

---

## 8. 전체 요청 처리 흐름

<!-- 담당: 애영 / 최종 통합 -->

예상 흐름:

사용자 요청
→ FastAPI
→ Redis Queue
→ AI Worker
→ 결과 저장

---

## 9. Event-Driven Architecture 설계도

<!-- 담당: 성규 -->
<!-- 최종 이미지 경로: docs/images/9일차_event_driven_architecture.png -->

이미지 삽입 예정

---

## 10. 설계 선택 이유 및 기대 효과

<!-- 담당: 애영 / 팀원 작성 내용 통합 후 정리 -->

---

## 11. 최종 완료 조건 확인

- [ ] FastAPI + Redis 기반 Event-Driven Architecture 학습 내용 정리
- [ ] Excalidraw 아키텍처 설계도 작성 및 이미지 삽입
- [ ] FastAPI와 AI Worker 역할 분리 표현
- [ ] Redis Queue(작업 대기열) 구조 표현
- [ ] 팀원별 담당 내용 통합
- [ ] 최종 PR을 통해 main 브랜치에 병합

---

## 12. 참고 자료

<!-- 각 담당자가 조사한 참고 자료를 최종 통합 단계에서 정리 -->
