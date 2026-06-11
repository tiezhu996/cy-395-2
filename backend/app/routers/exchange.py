from datetime import date, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.services.exchange_service import historical_rates, latest_rate, list_currencies

router = APIRouter(prefix="/api/v1/exchange", tags=["汇率查询"])


@router.get("/latest")
def latest(pairs: list[str] = Query(default=["USD/CNY"]), db: Session = Depends(get_db)):
    result = []
    for pair in pairs:
        base, quote = pair.split("/")
        rate = latest_rate(db, base, quote)
        if rate:
            result.append({"base": rate.base, "quote": rate.quote, "rate": rate.rate, "date": rate.rate_date})
    return result


@router.get("/history")
def history(base: str = "USD", quote: str = "CNY", start: date = date.today() - timedelta(days=7), end: date = date.today(), db: Session = Depends(get_db)):
    return historical_rates(db, base, quote, start, end)


@router.get("/currencies")
def currencies():
    return list_currencies()
