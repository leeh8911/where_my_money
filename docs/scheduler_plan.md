# 결제 예정 알림 스케줄러 계획

현재 상태:
- `GET /alerts/preview` 구현 (알림 후보 생성)

다음 구현:
1. APScheduler 또는 cron으로 하루 1~2회 실행
2. `billing_upcoming` 결과 중 D-3/D-1/D-day 필터
3. Discord로 전송
4. 발송 중복 방지 키(`card_id + due_day + sent_date`) 저장

임시 운영:
- 수동으로 `/alerts/preview` 호출해 알림 대상 점검 가능
