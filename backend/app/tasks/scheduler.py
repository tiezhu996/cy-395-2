from datetime import date
import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.models.base import SessionLocal
from app.models.entities import ExchangeRate
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


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_rates, "interval", hours=1, id="exchange-rate-refresh", replace_existing=True)
    scheduler.start()
    return scheduler
