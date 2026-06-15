from fastapi import APIRouter

from agent_orchestration_system.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthcheck() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
    }


@router.get("/readyz")
def readiness() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ready",
        "service": settings.otel_service_name,
    }

