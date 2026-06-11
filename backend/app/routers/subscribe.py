from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.schemas.subscribe import SubscriptionCreate
from app.services.subscription_service import create_subscription, list_subscriptions

router = APIRouter(prefix="/api/v1/subscribe", tags=["订阅通知"])


@router.post("")
def create(payload: SubscriptionCreate, request: Request, db: Session = Depends(get_db)):
    return create_subscription(db, request.state.client_id, payload)


@router.get("")
def list_all(request: Request, db: Session = Depends(get_db)):
    return list_subscriptions(db, request.state.client_id)
