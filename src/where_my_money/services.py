from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
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
    original_tx_id: str | None = None
    installment_months: int = 1


class TransactionSyncProvider(Protocol):
    def fetch(self) -> list[dict]:
        ...


class MockSyncProvider:
    """외부 API 연동 전까지 사용할 mock provider."""

    def __init__(self, tz: ZoneInfo):
        self.tz = tz

    def fetch(self) -> list[dict]:
        now = datetime.now(self.tz)
        return [
            {
                "tx_id": "sync_tx_1",
                "card_id": "card_kb",
                "approved_at": now,
                "amount": 4900,
                "merchant": "편의점",
                "category": "식비",
                "status": "approved",
                "original_tx_id": None,
                "installment_months": 1,
            }
        ]


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
            Transaction("tx4", "card_kb", now.replace(hour=7, minute=50), 120000, "가전", "쇼핑", installment_months=3),
            Transaction("tx5", "card_kb", now.replace(hour=9, minute=0), 3000, "편의점 취소", "식비", status="cancelled", original_tx_id="tx3"),
        ]
        self.sync_provider: TransactionSyncProvider = MockSyncProvider(self.tz)

    def _cycle_amount(self, tx: Transaction) -> float:
        return tx.amount / max(tx.installment_months, 1)

    def _is_current_cycle(self, tx: Transaction, billing_day: int) -> bool:
        """간단한 청구주기 계산: billing_day+1 ~ 다음 billing_day."""
        dt = tx.approved_at.astimezone(self.tz)
        now = datetime.now(self.tz)
        if now.day > billing_day:
            cycle_start = datetime(now.year, now.month, billing_day + 1, tzinfo=self.tz)
        else:
            prev_month = now.month - 1 or 12
            prev_year = now.year - 1 if now.month == 1 else now.year
            cycle_start = datetime(prev_year, prev_month, billing_day + 1, tzinfo=self.tz)
        return dt >= cycle_start

    def _net_transactions(self, txs: list[Transaction]) -> list[Transaction]:
        """취소 거래를 원거래와 매핑해 상계 처리한다."""
        by_id = {tx.tx_id: tx for tx in txs}
        cancelled_amount_by_origin: dict[str, float] = defaultdict(float)
        for tx in txs:
            if tx.status == "cancelled" and tx.original_tx_id:
                cancelled_amount_by_origin[tx.original_tx_id] += tx.amount

        net = []
        for tx in txs:
            if tx.status != "approved":
                continue
            cancelled = cancelled_amount_by_origin.get(tx.tx_id, 0.0)
            net_amount = max(tx.amount - cancelled, 0.0)
            if net_amount == 0:
                continue
            cloned = Transaction(
                tx_id=tx.tx_id,
                card_id=tx.card_id,
                approved_at=tx.approved_at,
                amount=net_amount,
                merchant=tx.merchant,
                category=tx.category,
                status="approved",
                installment_months=tx.installment_months,
            )
            net.append(cloned)
        return net

    def _today_transactions(self) -> list[Transaction]:
        today = datetime.now(self.tz).date()
        txs = [tx for tx in self.transactions if tx.approved_at.astimezone(self.tz).date() == today]
        return self._net_transactions(txs)

    def spend_today(self) -> dict:
        txs = self._today_transactions()
        total = sum(self._cycle_amount(tx) for tx in txs)
        by_card: dict[str, float] = defaultdict(float)
        by_category: dict[str, float] = defaultdict(float)
        for tx in txs:
            cycle_amount = self._cycle_amount(tx)
            by_card[tx.card_id] += cycle_amount
            by_category[tx.category] += cycle_amount
        return {
            "date": str(datetime.now(self.tz).date()),
            "total": float(round(total, 2)),
            "by_card": [
                {
                    "card_id": cid,
                    "alias": self.cards[cid].alias,
                    "amount": float(round(amount, 2)),
                }
                for cid, amount in by_card.items()
            ],
            "by_category": [
                {"category": c, "amount": float(round(a, 2))} for c, a in by_category.items()
            ],
        }

    def billing_upcoming(self) -> dict:
        now = datetime.now(self.tz)
        d = now.day
        result = []
        net_txs = self._net_transactions(self.transactions)
        for card in self.cards.values():
            if not card.is_active:
                continue
            amount = sum(
                self._cycle_amount(tx)
                for tx in net_txs
                if tx.card_id == card.card_id and self._is_current_cycle(tx, card.billing_day)
            )
            dday = card.billing_day - d
            result.append(
                {
                    "card_id": card.card_id,
                    "alias": card.alias,
                    "due_day": card.billing_day,
                    "dday": f"D-{dday}" if dday > 0 else ("D-day" if dday == 0 else f"D+{-dday}"),
                    "expected_amount": float(round(amount, 2)),
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

    def create_card(self, card_id: str, issuer: str, alias: str, billing_day: int) -> dict:
        if card_id in self.cards:
            raise ValueError("card already exists")
        if not (1 <= billing_day <= 28):
            raise ValueError("billing_day must be 1..28")
        card = Card(card_id=card_id, issuer=issuer, alias=alias, billing_day=billing_day)
        self.cards[card_id] = card
        return {
            "card_id": card.card_id,
            "issuer": card.issuer,
            "alias": card.alias,
            "billing_day": card.billing_day,
            "is_active": card.is_active,
        }

    def delete_card(self, card_id: str) -> dict:
        card = self.cards.get(card_id)
        if not card:
            raise ValueError("card not found")
        card.is_active = False
        return {"card_id": card_id, "is_active": False}

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
        net_txs = self._net_transactions(self.transactions)
        items = []
        for c in self.cards.values():
            if not c.is_active:
                continue
            amount = sum(
                self._cycle_amount(tx)
                for tx in net_txs
                if tx.card_id == c.card_id and tx.approved_at.year == now.year and tx.approved_at.month == now.month
            )
            items.append(
                {
                    "card_id": c.card_id,
                    "alias": c.alias,
                    "amount": float(round(amount, 2)),
                }
            )
        return {"period": period, "items": items}

    def sync_transactions(self) -> dict:
        payload = self.sync_provider.fetch()
        inserted = 0
        existing_ids = {tx.tx_id for tx in self.transactions}
        for row in payload:
            if row["tx_id"] in existing_ids:
                continue
            self.transactions.append(
                Transaction(
                    tx_id=row["tx_id"],
                    card_id=row["card_id"],
                    approved_at=row["approved_at"],
                    amount=float(row["amount"]),
                    merchant=row["merchant"],
                    category=row["category"],
                    status=row.get("status", "approved"),
                    original_tx_id=row.get("original_tx_id"),
                    installment_months=int(row.get("installment_months", 1)),
                )
            )
            inserted += 1
        return {"inserted": inserted, "total": len(self.transactions)}

    def alert_preview(self) -> dict:
        alerts = []
        for item in self.billing_upcoming()["items"]:
            if item["dday"] in {"D-3", "D-1", "D-day"}:
                alerts.append({
                    "type": "billing_due",
                    "message": f"{item['alias']} 결제 {item['dday']} / 예상 {item['expected_amount']:.0f}원",
                })
        return {"alerts": alerts}
