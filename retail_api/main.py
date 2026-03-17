from fastapi import FastAPI

from retail_api.common.middleware import RequestIdMiddleware
from retail_api.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)
    app.add_middleware(RequestIdMiddleware)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
