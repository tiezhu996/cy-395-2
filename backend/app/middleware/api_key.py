from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.config import settings
from app.constants import errors
from app.models.base import SessionLocal
from app.models.entities import ApiClient
from app.services.api_key_service import find_client, record_call


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/health", "/docs", "/openapi.json", "/api/v1/apikey/register"} or request.url.path.startswith("/docs"):
            return await call_next(request)
        api_key = request.headers.get("X-API-Key", settings.default_api_key)
        db = SessionLocal()
        try:
            client = find_client(db, api_key)
            if client is None and api_key == settings.default_api_key:
                client = ApiClient(name="demo", api_key=settings.default_api_key)
                db.add(client)
                db.commit()
                db.refresh(client)
            if client is None:
                return JSONResponse({"code": errors.UNAUTHORIZED, "message": "缺少或无效的 API Key"}, status_code=401)
            request.state.client_id = client.id
            response = await call_next(request)
            record_call(db, client.id, request.url.path)
            return response
        finally:
            db.close()
