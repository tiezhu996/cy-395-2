from datetime import date
import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.models.base import SessionLocal
from app.models.entities import ExchangeRate, Subscription
from app.services.subscription_service import should_notify, simulate_notify
from app.utils.logger import logger


def update_rates() -> None:
    db = SessionLocal()
    try:
        response = httpx.get(settings.exchange_api_url, timeout=8)
        data = response.json()
        rates = data.get("rates", {})
        for quote, rate in rates.items():
            if len(quote) == 3 and isinstance(rate, (int, float)):
                db.add(ExchangeRate(base="USD", quote=quote, rate=float(rate), rate_date=date.today()))
        db.commit()
        logger.info("exchange rates refreshed count=%s", len(rates))
    except Exception as exc:
        logger.warning("exchange rate refresh skipped: %s", exc)
    finally:
        db.close()


def check_subscriptions() -> None:
    db = SessionLocal()
    try:
        subscriptions = db.query(Subscription).filter(Subscription.active.is_(True)).all()
        if not subscriptions:
            return
        pairs = {(sub.base, sub.quote) for sub in subscriptions}
        latest_rates: dict[tuple[str, str], float] = {}
        for base, quote in pairs:
            rate_row = (
                db.query(ExchangeRate)
                .filter(ExchangeRate.base == base, ExchangeRate.quote == quote)
                .order_by(ExchangeRate.rate_date.desc())
                .first()
            )
            if rate_row:
                latest_rates[(base, quote)] = rate_row.rate
        for sub in subscriptions:
            key = (sub.base, sub.quote)
            actual_rate = latest_rates.get(key)
            if actual_rate is None:
                continue
            if should_notify(sub, actual_rate):
                simulate_notify(sub, actual_rate)
    except Exception as exc:
        logger.warning("subscription check failed: %s", exc)
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_rates, "interval", hours=1, id="exchange-rate-refresh", replace_existing=True)
    scheduler.add_job(check_subscriptions, "interval", hours=1, id="subscription-check", replace_existing=True)
    scheduler.start()
    return scheduler
