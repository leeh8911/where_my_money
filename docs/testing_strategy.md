# 테스트 전략 / 커버리지 기준

## 커버리지 기준 (초안)
- 핵심 집계 로직(`services.py`) 라인 커버리지 85% 이상 목표
- API smoke 테스트 전 엔드포인트 최소 1개 케이스 유지

## 회귀 테스트 세트
- 취소거래 상계
- 할부 당월 반영
- 카드 비활성 시 summary/billing 제외
- alias/active 업데이트 에러 처리
- sync 중복 tx_id 무시

## 실행 명령
```bash
./.venv/bin/pytest -q
```
