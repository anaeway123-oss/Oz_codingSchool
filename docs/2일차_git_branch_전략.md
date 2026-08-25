# Git Branch 전략

## 1. Git Branch란?

Git의 Branch는 하나의 프로젝트에서 여러 작업을 독립적으로 진행할 수 있도록 만들어 주는 기능입니다.

여러 명의 개발자가 하나의 프로젝트를 진행할 때 각자 별도의 Branch에서 작업하면 다른 팀원의 코드에 영향을 주지 않고 기능을 개발할 수 있습니다.

작업이 완료되면 해당 Branch의 내용을 main Branch에 병합(Merge)하여 하나의 프로젝트로 합칠 수 있습니다.

---

## 2. Git Flow

Git Flow는 개발, 기능 추가, 출시 준비, 긴급 수정 등의 작업을 목적에 따라 여러 Branch로 나누어 관리하는 전략입니다.

### 주요 Branch

* `main` : 실제 배포되는 안정적인 코드
* `develop` : 다음 버전 개발을 위한 코드
* `feature` : 새로운 기능을 개발하는 Branch
* `release` : 새로운 버전의 출시를 준비하는 Branch
* `hotfix` : 배포된 코드의 긴급한 오류를 수정하는 Branch

### 장점

* 각 Branch의 역할이 명확하여 체계적인 관리가 가능합니다.
* 여러 명이 동시에 개발하는 프로젝트에 유용합니다.
* 출시 버전을 안정적으로 관리하기 좋습니다.

### 단점

* 사용하는 Branch가 많아 관리가 복잡할 수 있습니다.
* 작은 프로젝트에서는 불필요하게 복잡할 수 있습니다.

---

## 3. GitHub Flow

GitHub Flow는 Git Flow보다 단순한 Branch 전략입니다.

기본이 되는 `main` Branch를 유지하면서 새로운 기능이나 수정 작업이 필요할 때 별도의 Branch를 생성합니다.

작업이 완료되면 GitHub에 Push한 뒤 Pull Request(PR)를 생성합니다. 코드 리뷰와 확인을 거쳐 문제가 없다면 해당 Branch를 `main` Branch에 Merge합니다.

### 기본 흐름

`main → Branch 생성 → 작업 → Commit → Push → Pull Request → Review → main에 Merge`

### 장점

* Branch 구조가 단순하여 이해하기 쉽습니다.
* 기능을 빠르게 개발하고 반영할 수 있습니다.
* 작은 팀이나 지속적으로 업데이트하는 프로젝트에 적합합니다.

### 단점

* 복잡한 버전 관리가 필요한 프로젝트에서는 부족할 수 있습니다.
* `main`에 자주 병합되므로 코드 리뷰와 테스트가 중요합니다.

---

## 4. Git Flow와 GitHub Flow 비교

| 구분        | Git Flow                                | GitHub Flow         |
| --------- | --------------------------------------- | ------------------- |
| Branch 구조 | 여러 종류의 Branch 사용                        | 단순한 Branch 구조       |
| 주요 Branch | main, develop, feature, release, hotfix | main, feature       |
| 특징        | 체계적인 버전 관리                              | 빠르고 간단한 개발          |
| 장점        | 안정적인 버전 및 배포 관리                         | 이해하기 쉽고 빠름          |
| 적합한 프로젝트  | 규모가 크고 버전 관리가 중요한 프로젝트                  | 빠른 개발과 배포가 필요한 프로젝트 |

---

## 5. 정리

Git Flow와 GitHub Flow는 여러 개발자가 하나의 프로젝트를 안전하게 관리하기 위한 Branch 전략입니다.

Git Flow는 여러 종류의 Branch를 사용하여 개발과 배포 과정을 체계적으로 관리할 수 있다는 장점이 있습니다.

반면 GitHub Flow는 `main`과 작업용 Branch를 중심으로 운영하여 구조가 간단하고 빠르게 개발할 수 있습니다.

따라서 프로젝트의 규모와 배포 방식, 팀의 작업 방식에 따라 적절한 Branch 전략을 선택하는 것이 중요합니다.
