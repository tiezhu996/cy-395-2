from sqlalchemy.orm import Session
from app.models.entities import Subscription
from app.schemas.subscribe import SubscriptionCreate
from app.utils.logger import logger


def create_subscription(db: Session, client_id: int, payload: SubscriptionCreate) -> Subscription:
    sub = Subscription(
        client_id=client_id,
        base=payload.base.upper(),
        quote=payload.quote.upper(),
        target_rate=payload.target_rate,
        direction=payload.direction.value,
        notify_url=payload.notify_url,
        email=payload.email,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def list_subscriptions(db: Session, client_id: int) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.client_id == client_id).all()


def should_notify(subscription: Subscription, actual_rate: float) -> bool:
    direction = subscription.direction or "both"
    if direction == "down":
        return actual_rate <= subscription.target_rate
    return actual_rate >= subscription.target_rate


def simulate_notify(subscription: Subscription, actual_rate: float) -> None:
    direction_label = {"both": "涨跌均通知", "up": "涨破", "down": "跌破"}.get(subscription.direction, subscription.direction)
    logger.info(
        "simulate notification subscription=%s base=%s quote=%s target_rate=%s direction=%s actual_rate=%s webhook=%s email=%s",
        subscription.id,
        subscription.base,
        subscription.quote,
        subscription.target_rate,
        direction_label,
        actual_rate,
        subscription.notify_url,
        subscription.email,
    )
