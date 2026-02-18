# 외부 데이터소스 어댑터 설계 (카드/은행/중계)

## 목표
카드사/은행/마이데이터 공급자별 차이를 `Adapter` 레이어로 격리한다.

## 인터페이스
- `fetch() -> list[transaction_dict]`
- 출력 스키마 표준화:
  - tx_id, card_id, approved_at, amount, merchant, category, status, original_tx_id, installment_months

## 구현 순서
1. MockSyncProvider (완료)
2. CSV/파일 기반 로컬 어댑터
3. 중계 API(마이데이터) 어댑터
4. 카드사/은행별 전용 어댑터 (필요시)

## 검증 포인트
- 중복 tx_id 무시
- 시간대 변환(KST)
- 취소/부분취소 매핑
- installment_months 누락시 1로 처리
