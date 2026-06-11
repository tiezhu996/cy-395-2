from sqlalchemy.orm import Session
from app.models.entities import Subscription
from app.schemas.subscribe import SubscriptionCreate
from app.utils.logger import logger


def create_subscription(db: Session, client_id: int, payload: SubscriptionCreate) -> Subscription:
    sub = Subscription(client_id=client_id, base=payload.base.upper(), quote=payload.quote.upper(), target_rate=payload.target_rate, notify_url=payload.notify_url, email=payload.email)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def list_subscriptions(db: Session, client_id: int) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.client_id == client_id).all()


def simulate_notify(subscription: Subscription, actual_rate: float) -> None:
    logger.info("simulate notification subscription=%s actual_rate=%s webhook=%s email=%s", subscription.id, actual_rate, subscription.notify_url, subscription.email)
