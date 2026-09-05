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

팀원별 4일차 초안과 테스트 근거가 `integration/day4-readme-merge`에 모두 모인 뒤
애영님이 실제 확인된 결과만 취합하여 최종 작성할 예정입니다.

현재는 아직 팀원 초안이 모두 작성되기 전이므로
확인하지 않은 내용을 임의로 작성하지 않습니다.
