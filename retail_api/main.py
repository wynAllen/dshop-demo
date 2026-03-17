import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from retail_api.common.exceptions import AppException
from retail_api.common.middleware import RequestIdMiddleware
from retail_api.config import settings

logger = logging.getLogger(__name__)


class _RegisterBody(BaseModel):
    email: str
    password: str


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(RequestIdMiddleware)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/api/v1/users/register")
    def _register_stub(_body: _RegisterBody):
        return {"id": "stub", "email": _body.email}

    @app.exception_handler(AppException)
    def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": exc.code, "message": exc.message, "details": exc.details},
        )

    @app.exception_handler(StarletteHTTPException)
    def http_exception_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        code = "NOT_FOUND" if exc.status_code == 404 else f"HTTP_{exc.status_code}"
        detail = exc.detail
        if isinstance(detail, dict):
            message = detail.get("message", str(detail))
        else:
            message = str(detail) if detail else "Request failed"
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": code, "message": message, "details": {}},
        )

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {"errors": exc.errors()},
            },
        )

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "Unhandled exception",
            extra={"request_id": request_id},
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            },
        )

    return app
