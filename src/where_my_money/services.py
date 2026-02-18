from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class Card:
    card_id: str
    issuer: str
    alias: str
    billing_day: int
    is_active: bool = True


@dataclass
class Transaction:
    tx_id: str
    card_id: str
    approved_at: datetime
    amount: float
    merchant: str
    category: str
    status: str = "approved"  # approved | cancelled


class MoneyService:
    """MVP in-memory service. DB 연동 전까지 샘플 데이터로 동작."""

    def __init__(self, timezone: str):
        self.tz = ZoneInfo(timezone)
        now = datetime.now(self.tz)
        self.cards = {
            "card_hyundai": Card("card_hyundai", "Hyundai", "생활비카드", 25),
            "card_kb": Card("card_kb", "KB", "고정비카드", 14),
        }
        self.transactions = [
            Transaction("tx1", "card_hyundai", now.replace(hour=9, minute=30), 12000, "스타벅스", "식비"),
            Transaction("tx2", "card_hyundai", now.replace(hour=12, minute=0), 8500, "편의점", "식비"),
            Transaction("tx3", "card_kb", now.replace(hour=8, minute=10), 1550, "지하철", "교통"),
        ]

    def _today_transactions(self) -> list[Transaction]:
        today = datetime.now(self.tz).date()
        return [
            tx
            for tx in self.transactions
            if tx.approved_at.astimezone(self.tz).date() == today and tx.status == "approved"
        ]

    def spend_today(self) -> dict:
        txs = self._today_transactions()
        total = sum(tx.amount for tx in txs)
        by_card: dict[str, float] = defaultdict(float)
        by_category: dict[str, float] = defaultdict(float)
        for tx in txs:
            by_card[tx.card_id] += tx.amount
            by_category[tx.category] += tx.amount
        return {
            "date": str(datetime.now(self.tz).date()),
            "total": float(total),
            "by_card": [
                {
                    "card_id": cid,
                    "alias": self.cards[cid].alias,
                    "amount": float(amount),
                }
                for cid, amount in by_card.items()
            ],
            "by_category": [
                {"category": c, "amount": float(a)} for c, a in by_category.items()
            ],
        }

    def billing_upcoming(self) -> dict:
        now = datetime.now(self.tz)
        y, m, d = now.year, now.month, now.day
        result = []
        this_month_txs = [
            tx for tx in self.transactions if tx.approved_at.year == y and tx.approved_at.month == m and tx.status == "approved"
        ]
        for card in self.cards.values():
            amount = sum(tx.amount for tx in this_month_txs if tx.card_id == card.card_id)
            dday = card.billing_day - d
            result.append(
                {
                    "card_id": card.card_id,
                    "alias": card.alias,
                    "due_day": card.billing_day,
                    "dday": f"D-{dday}" if dday > 0 else ("D-day" if dday == 0 else f"D+{-dday}"),
                    "expected_amount": float(amount),
                }
            )
        return {"items": result}

    def list_cards(self) -> list[dict]:
        return [
            {
                "card_id": c.card_id,
                "issuer": c.issuer,
                "alias": c.alias,
                "billing_day": c.billing_day,
                "is_active": c.is_active,
            }
            for c in self.cards.values()
        ]

    def update_card_alias(self, card_id: str, alias: str) -> dict:
        card = self.cards.get(card_id)
        if not card:
            raise ValueError("card not found")
        card.alias = alias
        return {"card_id": card.card_id, "alias": card.alias}

    def update_card_active(self, card_id: str, is_active: bool) -> dict:
        card = self.cards.get(card_id)
        if not card:
            raise ValueError("card not found")
        card.is_active = is_active
        return {"card_id": card.card_id, "is_active": card.is_active}

    def cards_summary(self, period: str = "this_month") -> dict:
        if period != "this_month":
            return {"period": period, "items": []}
        now = datetime.now(self.tz)
        items = []
        for c in self.cards.values():
            amount = sum(
                tx.amount
                for tx in self.transactions
                if tx.card_id == c.card_id and tx.approved_at.year == now.year and tx.approved_at.month == now.month and tx.status == "approved"
            )
            items.append(
                {
                    "card_id": c.card_id,
                    "alias": c.alias,
                    "amount": float(amount),
                }
            )
        return {"period": period, "items": items}
