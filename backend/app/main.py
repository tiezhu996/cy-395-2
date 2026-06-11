from fastapi import FastAPI
from app.middleware.api_key import ApiKeyMiddleware
from app.models.base import Base, SessionLocal, engine
from app.routers import apikey, convert, exchange, subscribe
from app.services.exchange_service import seed_rates
from app.tasks.scheduler import start_scheduler
from app.utils.exceptions import register_exception_handlers

app = FastAPI(title="Forex API", description="汇率换算与定时推送 API 服务", version="1.0.0")
app.add_middleware(ApiKeyMiddleware)
register_exception_handlers(app)
app.include_router(apikey.router)
app.include_router(exchange.router)
app.include_router(convert.router)
app.include_router(subscribe.router)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_rates(db)
    finally:
        db.close()
    start_scheduler()


@app.get("/health")
def health():
    return {"status": "ok"}
