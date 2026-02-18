# where_my_money 완료 내역

> 원칙: `docs/todos.md`에서 완료된 항목만 이관
> 기록: 각 항목에 완료 시점(로컬 시간, Asia/Seoul) 기재

## Pre-Phase (기초 세팅)
- [x] Python 패키지 템플릿 초기 구성 완료 — **2026-02-18 09:31**
  - `pyproject.toml`, `src/`, `tests/`, `README.md`, `.gitignore`
- [x] 원격 저장소 첫 push 완료 (`main`) — **2026-02-18 09:39**
  - repo: `git@github.com:leeh8911/where_my_money.git`
- [x] 개발 가드레일 스킬 추가 — **2026-02-18 09:52**
  - `skills/development-guardrails/SKILL.md`
- [x] 로그 파일 시작 — **2026-02-18 09:52**
  - `logs/2026-02-18.md`

## Phase 0 (프로젝트 기반 정리) — 완료
- [x] API 서버 기본 구조(FastAPI) 생성 — **2026-02-18 10:01 KST**
  - `src/where_my_money/main.py`, `src/where_my_money/services.py`, `src/where_my_money/settings.py`
- [x] 환경변수 템플릿(`.env.example`) 추가 — **2026-02-18 10:01 KST**
- [x] DB 선택 및 마이그레이션 도구 결정 — **2026-02-18 10:01 KST**
  - SQLite + Alembic (`docs/architecture.md`)
- [x] 공통 에러 응답 포맷 정의 — **2026-02-18 10:01 KST**
  - `{ "error": { "code", "message", "details" } }`
- [x] 로깅 포맷 표준화(text/json) — **2026-02-18 10:01 KST**
  - `LOG_FORMAT` 환경변수 + 아키텍처 문서화

## Phase 1 (1차 MVP 구현) — 완료
- [x] `GET /spend/today` 구현 — **2026-02-18 10:01 KST**
- [x] 오늘 총 지출 계산 로직 구현 — **2026-02-18 10:01 KST**
- [x] 카드별 오늘 지출 집계 구현 — **2026-02-18 10:01 KST**
- [x] 카테고리별 오늘 지출 집계 구현 — **2026-02-18 10:01 KST**
- [x] `GET /billing/upcoming` 구현 — **2026-02-18 10:01 KST**
- [x] 카드별 결제일 필드 모델링 — **2026-02-18 10:01 KST**
- [x] 이번 달 결제 예정 금액 계산 로직 구현(기본형) — **2026-02-18 10:01 KST**
- [x] D-day(`D-3`, `D-1`, `D-day`) 계산값 포함 — **2026-02-18 10:01 KST**
- [x] `GET /cards` 구현 — **2026-02-18 10:01 KST**
- [x] 카드 등록/조회 모델 구현(메모리 모델) — **2026-02-18 10:01 KST**
- [x] 카드 별칭(alias) 변경 API 구현 — **2026-02-18 10:01 KST**
- [x] 카드 활성/비활성 API 구현 — **2026-02-18 10:01 KST**
- [x] 카드별 사용량 API 구현 (`GET /cards/summary`) — **2026-02-18 10:01 KST**
- [x] 취소 거래 상계 처리 규칙 고도화(원거래 매핑) — **2026-02-18 10:08 KST**
- [x] 카드사별 청구주기(이용기간) 계산 로직 반영(기본형) — **2026-02-18 10:08 KST**
- [x] 할부 반영 결제 예정 금액 계산 고도화(월할 계산) — **2026-02-18 10:08 KST**
- [x] 카드 등록 API 구현 (`POST /cards`) — **2026-02-18 10:08 KST**
- [x] 카드 삭제 정책 확정 및 구현 (`DELETE /cards/{card_id}` soft delete) — **2026-02-18 10:08 KST**
- [x] API 테스트 추가 및 실행 — **2026-02-18 10:08 KST**
  - 결과: `11 passed`

## Phase 2 (연동/자동화) — 부분 완료
- [x] 거래 동기화 엔드포인트 `POST /sync/transactions` 고도화(mock provider 포함) — **2026-02-18 10:08 KST**
- [x] 외부 데이터소스 어댑터 인터페이스 설계(카드/은행/중계) — **2026-02-18 10:08 KST**
  - `docs/integration_adapter.md`
- [x] Discord 출력 포맷 설계 (요약/상세) — **2026-02-18 10:08 KST**
  - `docs/discord_output_format.md`
- [x] Notion 일자별 로그 자동 적재 초안 — **2026-02-18 10:08 KST**
  - `docs/notion_logging_draft.md`

## Phase 3 (신뢰성/운영) — 부분 완료
- [x] 테스트 커버리지 기준 수립(문서) — **2026-02-18 10:08 KST**
  - `docs/testing_strategy.md`
- [x] 집계/정산 회귀 테스트 세트 1차 구축 — **2026-02-18 10:08 KST**
  - 취소/할부/카드삭제/sync/alerts 회귀 포함
- [x] 알림 후보 생성 로직 추가 (`GET /alerts/preview`) — **2026-02-18 10:08 KST**
- [x] 운영 체크리스트 문서화 — **2026-02-18 10:08 KST**
  - `docs/ops_checklist.md`, `docs/scheduler_plan.md`
