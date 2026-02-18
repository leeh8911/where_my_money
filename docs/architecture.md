# where_my_money 아키텍처 결정 (MVP)

## 1) API 프레임워크
- FastAPI 채택
- 이유: 타입 기반 스키마, 테스트 용이성, 빠른 MVP 개발

## 2) DB / 마이그레이션
- DB: SQLite (초기)
- 마이그레이션: Alembic
- 이유: 로컬 개발 단순성 + 이후 PostgreSQL 전환 용이

## 3) 로깅 포맷
- 기본: text
- 옵션: json (환경변수 `LOG_FORMAT=json`)

## 4) 공통 에러 포맷
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## 5) 시간 기준
- 기본 타임존: Asia/Seoul
- 일자 집계(오늘 지출)는 로컬 타임존 기준
