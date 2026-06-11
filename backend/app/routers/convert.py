from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.schemas.exchange import ConvertRequest
from app.services.exchange_service import convert

router = APIRouter(prefix="/api/v1/convert", tags=["货币换算"])


@router.post("")
def convert_currency(payload: ConvertRequest, db: Session = Depends(get_db)):
    return convert(db, payload.source, payload.target, payload.amount)
