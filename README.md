# where_my_money

Python package template for tracking and analyzing personal spending.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
pytest -q
```

## Run API server

```bash
uvicorn where_my_money.main:app --reload
```

주요 엔드포인트:
- `GET /spend/today`
- `GET /billing/upcoming`
- `GET /cards`
- `PATCH /cards/{card_id}/alias`
- `PATCH /cards/{card_id}/active`
- `GET /cards/summary`

## Development guardrails

- Skill: `skills/development-guardrails/SKILL.md`
- Rule: 개발 변경 시 테스트 작성/실행 + 작업 로그(`logs/YYYY-MM-DD.md`) 기록 + 자주 커밋
