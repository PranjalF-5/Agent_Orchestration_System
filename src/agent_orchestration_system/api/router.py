from fastapi import APIRouter

from agent_orchestration_system.api.routes.health import router as health_router
from agent_orchestration_system.api.routes.tasks import router as tasks_router
from agent_orchestration_system.api.routes.workflows import router as workflows_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(tasks_router)
api_router.include_router(workflows_router)
