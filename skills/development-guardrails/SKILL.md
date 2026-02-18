---
name: development-guardrails
description: Use for any development task in this repository. Enforce small frequent commits with work logs, and require tests to be created/executed before completion.
---

# Development Guardrails

## 목적
이 저장소에서 개발 작업 품질을 일정하게 유지한다.

## 필수 규칙
1. **작업 단위마다 커밋**한다.
   - 기능/수정이 확인 가능한 최소 단위로 자주 커밋한다.
   - 커밋 메시지는 무엇을 바꿨는지 명확하게 쓴다.
2. **커밋 로그 기록**을 남긴다.
   - `logs/YYYY-MM-DD.md`에 작업 요약/테스트 결과/다음 액션을 남긴다.
3. **테스트 우선/최소 테스트 보장**.
   - 코드 변경 시 관련 테스트를 반드시 추가하거나 보강한다.
   - 완료 전 테스트 실행 결과를 확인한다.
4. **TODO 운영 규칙 준수**.
   - 할 일은 `docs/todos.md`에서 관리한다.
   - 완료된 항목은 `docs/todos_done.md`로 이동하고 완료 시점(일시)을 기록한다.
   - 항목이 많아지면 `docs/todos_done_phaseX.md` 형식으로 phase별 분리 가능하다.
5. **성공 주장 금지**.
   - 테스트 실행 결과 없이 "완료", "정상 동작"을 주장하지 않는다.

## 기본 워크플로우
1. 변경 범위 정의
2. 테스트 작성 또는 기존 테스트 보강
3. 구현
4. 테스트 실행
5. `logs/YYYY-MM-DD.md` 기록
6. 커밋

## 최소 테스트 명령
```bash
python -m pytest -q
```

## 커밋 메시지 예시
- `feat: add daily spending summary endpoint`
- `fix: handle cancelled transactions in totals`
- `test: add card alias validation cases`

## 로그 템플릿 (`logs/YYYY-MM-DD.md`)
```md
## [HH:MM] 작업 제목
- 변경 내용:
- 테스트:
- 결과:
- 다음 액션:
```
