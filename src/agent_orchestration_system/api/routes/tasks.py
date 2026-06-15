from fastapi import APIRouter, status
import uuid

from agent_orchestration_system.api.schemas.tasks import TaskRequest, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def create_task(request: TaskRequest) -> TaskResponse:
    new_task_id = uuid.uuid4()
    return TaskResponse(task_id=new_task_id, status="pending")

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: uuid.UUID) -> TaskResponse:
    return TaskResponse(task_id=task_id, status="pending")
