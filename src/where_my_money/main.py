from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from where_my_money.settings import get_settings
from where_my_money.services import MoneyService

settings = get_settings()
service = MoneyService(settings.timezone)

app = FastAPI(title="where_my_money", version="0.1.0")


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"http_{exc.status_code}",
                "message": str(exc.detail),
                "details": {},
            }
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(_, exc: ValueError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "not_found",
                "message": str(exc),
                "details": {},
            }
        },
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/spend/today")
def spend_today():
    return service.spend_today()


@app.get("/billing/upcoming")
def billing_upcoming():
    return service.billing_upcoming()


@app.get("/cards")
def cards():
    return {"items": service.list_cards()}


@app.post("/cards")
def create_card(payload: dict):
    for key in ("card_id", "issuer", "alias", "billing_day"):
        if key not in payload:
            raise HTTPException(status_code=400, detail=f"{key} is required")
    return service.create_card(
        card_id=payload["card_id"],
        issuer=payload["issuer"],
        alias=payload["alias"],
        billing_day=int(payload["billing_day"]),
    )


@app.delete("/cards/{card_id}")
def delete_card(card_id: str):
    return service.delete_card(card_id)


@app.patch("/cards/{card_id}/alias")
def update_alias(card_id: str, payload: dict):
    alias = payload.get("alias")
    if not alias:
        raise HTTPException(status_code=400, detail="alias is required")
    return service.update_card_alias(card_id, alias)


@app.patch("/cards/{card_id}/active")
def update_active(card_id: str, payload: dict):
    if "is_active" not in payload:
        raise HTTPException(status_code=400, detail="is_active is required")
    return service.update_card_active(card_id, bool(payload["is_active"]))


@app.get("/cards/summary")
def cards_summary(period: str = "this_month"):
    return service.cards_summary(period=period)


@app.post("/sync/transactions")
def sync_transactions():
    return service.sync_transactions()


@app.get("/alerts/preview")
def alerts_preview():
    return service.alert_preview()
