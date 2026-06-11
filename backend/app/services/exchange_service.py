from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.constants.currencies import CURRENCIES
from app.models.entities import ExchangeRate


def list_currencies() -> list[dict]:
    return [{"code": code, "name": data[0], "symbol": data[1]} for code, data in CURRENCIES.items()]


def seed_rates(db: Session) -> None:
    if db.query(ExchangeRate).first():
        return
    samples = {"CNY": 7.18, "EUR": 0.92, "JPY": 156.2, "GBP": 0.79, "HKD": 7.82}
    today = date.today()
    for day in range(10):
        for quote, rate in samples.items():
            db.add(ExchangeRate(base="USD", quote=quote, rate=rate + day * 0.01, rate_date=today - timedelta(days=day)))
    db.commit()


def latest_rate(db: Session, base: str, quote: str) -> ExchangeRate | None:
    return db.query(ExchangeRate).filter(ExchangeRate.base == base.upper(), ExchangeRate.quote == quote.upper()).order_by(ExchangeRate.rate_date.desc()).first()


def historical_rates(db: Session, base: str, quote: str, start: date, end: date) -> list[ExchangeRate]:
    return db.query(ExchangeRate).filter(ExchangeRate.base == base.upper(), ExchangeRate.quote == quote.upper(), ExchangeRate.rate_date >= start, ExchangeRate.rate_date <= end).order_by(ExchangeRate.rate_date).all()


def convert(db: Session, source: str, target: str, amount: float) -> dict:
    source = source.upper()
    target = target.upper()
    if source == "USD":
        rate = latest_rate(db, "USD", target)
        chain = ["USD", target]
        final_rate = rate.rate if rate else 1
    elif target == "USD":
        rate = latest_rate(db, "USD", source)
        chain = [source, "USD"]
        final_rate = 1 / rate.rate if rate else 1
    else:
        source_rate = latest_rate(db, "USD", source)
        target_rate = latest_rate(db, "USD", target)
        chain = [source, "USD", target]
        final_rate = (target_rate.rate if target_rate else 1) / (source_rate.rate if source_rate else 1)
    return {"source": source, "target": target, "amount": amount, "converted_amount": round(amount * final_rate, 4), "rate": round(final_rate, 6), "chain": chain}
