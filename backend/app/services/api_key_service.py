import secrets
from sqlalchemy.orm import Session
from app.models.entities import ApiCall, ApiClient


def create_client(db: Session, name: str) -> ApiClient:
    client = ApiClient(name=name, api_key=secrets.token_urlsafe(24))
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def find_client(db: Session, api_key: str) -> ApiClient | None:
    return db.query(ApiClient).filter(ApiClient.api_key == api_key).first()


def record_call(db: Session, client_id: int, path: str) -> None:
    db.add(ApiCall(client_id=client_id, path=path))
    db.commit()


def call_stats(db: Session, client_id: int) -> dict:
    calls = db.query(ApiCall).filter(ApiCall.client_id == client_id).all()
    by_path: dict[str, int] = {}
    for call in calls:
        by_path[call.path] = by_path.get(call.path, 0) + 1
    return {"total": len(calls), "by_path": by_path}
