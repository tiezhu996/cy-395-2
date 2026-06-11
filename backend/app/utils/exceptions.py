from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.constants import errors
from app.utils.logger import logger


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def handle_exception(_: Request, exc: Exception):
        logger.exception("request failed: %s", exc)
        return JSONResponse(status_code=500, content={"code": errors.INTERNAL_ERROR, "message": str(exc)})
