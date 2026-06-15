from fastapi import FastAPI

from agent_orchestration_system.api.router import api_router
from agent_orchestration_system.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.include_router(api_router)
    return app

