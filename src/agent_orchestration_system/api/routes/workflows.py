from fastapi import APIRouter, Depends, HTTPException, status

from agent_orchestration_system.orchestration.models import (
    WorkflowCreateRequest,
    WorkflowRecord,
)
from agent_orchestration_system.orchestration.service import (
    InMemoryWorkflowService,
    WorkflowNotFoundError,
    get_workflow_service,
)

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowRecord, status_code=status.HTTP_201_CREATED)
def create_workflow(
    payload: WorkflowCreateRequest,
    workflow_service: InMemoryWorkflowService = Depends(get_workflow_service),
) -> WorkflowRecord:
    return workflow_service.create_workflow(payload)


@router.get("", response_model=list[WorkflowRecord])
def list_workflows(
    workflow_service: InMemoryWorkflowService = Depends(get_workflow_service),
) -> list[WorkflowRecord]:
    return workflow_service.list_workflows()


@router.get("/{workflow_id}", response_model=WorkflowRecord)
def get_workflow(
    workflow_id: str,
    workflow_service: InMemoryWorkflowService = Depends(get_workflow_service),
) -> WorkflowRecord:
    try:
        return workflow_service.get_workflow(workflow_id)
    except WorkflowNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found") from exc

