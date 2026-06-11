from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.schemas.apikey import ApiKeyResponse, RegisterRequest
from app.services.api_key_service import call_stats, create_client

router = APIRouter(prefix="/api/v1/apikey", tags=["API Key"])


@router.post("/register", response_model=ApiKeyResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    client = create_client(db, payload.name)
    return ApiKeyResponse(name=client.name, api_key=client.api_key)


@router.get("/stats")
def stats(request: Request, db: Session = Depends(get_db)):
    return call_stats(db, request.state.client_id)
