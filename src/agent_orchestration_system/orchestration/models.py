from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class WorkflowStage(str, Enum):
    supervisor = "supervisor"
    planner = "planner"
    executor = "executor"
    reviewer = "reviewer"


class WorkflowStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"


class WorkflowCreateRequest(BaseModel):
    objective: str = Field(..., min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)
    requested_by: str | None = None


class WorkflowRecord(BaseModel):
    workflow_id: str
    objective: str
    context: dict[str, Any]
    requested_by: str | None = None
    stages: list[WorkflowStage]
    status: WorkflowStatus

