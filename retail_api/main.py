import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from retail_api.common.exceptions import AppException
from retail_api.common.middleware import RequestIdMiddleware
from retail_api.config import settings
from retail_api.db.base import Base
from retail_api.db.session import engine
from retail_api.product import router as product_router
from retail_api.user import router as user_router
from retail_api.user.models import User  # noqa: F401 - register with Base
from retail_api.product.models import Product  # noqa: F401 - register with Base

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(RequestIdMiddleware)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(user_router.router)
    app.include_router(product_router.router)

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
