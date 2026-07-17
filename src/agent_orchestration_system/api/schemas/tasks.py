from typing import Any
from pydantic import BaseModel, Field
import uuid

class TaskRequest(BaseModel):
    prompt: str = Field(..., description="The main instruction for the agent")
    tenant_id: str = Field(..., description="Tenant ID for multi-tenancy isolation")
    config: dict[str, Any] = Field(default_factory=dict, description="Configuration overrides")

class TaskResponse(BaseModel):
    task_id: uuid.UUID = Field(..., description="Unique task identifier")
    status: str = Field(..., description="Task status (e.g., pending, completed)")
    result: Any = Field(None, description="Final result of the task execution")
    plan: str = Field(None, description="Generated plan by the agent")
