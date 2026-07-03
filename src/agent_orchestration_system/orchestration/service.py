from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session
from agent_orchestration_system.core.db import Task, SessionLocal
from agent_orchestration_system.orchestration.models import (
    WorkflowCreateRequest,
    WorkflowRecord,
    WorkflowStage,
    WorkflowStatus,
)

class WorkflowNotFoundError(Exception):
    """Raised when a workflow id cannot be found."""

class PostgresWorkflowService:
    def create_workflow(self, payload: WorkflowCreateRequest) -> WorkflowRecord:
        db: Session = SessionLocal()
        try:
            new_task = Task(
                tenant_id=payload.context.get("tenant_id", "default_tenant"),
                original_request=payload.objective,
                status="pending"
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            
            return self._to_record(new_task)
        finally:
            db.close()

    def get_workflow(self, workflow_id: str) -> WorkflowRecord:
        db: Session = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == workflow_id).first()
            if not task:
                raise WorkflowNotFoundError(workflow_id)
            return self._to_record(task)
        finally:
            db.close()

    def list_workflows(self) -> List[WorkflowRecord]:
        db: Session = SessionLocal()
        try:
            tasks = db.query(Task).all()
            return [self._to_record(t) for t in tasks]
        finally:
            db.close()
            
    def update_workflow_status(self, workflow_id: str, status: WorkflowStatus):
        db: Session = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == workflow_id).first()
            if task:
                task.status = status.value
                db.commit()
        finally:
            db.close()

    def _to_record(self, task: Task) -> WorkflowRecord:
        # Convert DB Task to Pydantic WorkflowRecord
        # Map DB status to Enum
        try:
            status = WorkflowStatus(task.status)
        except ValueError:
            status = WorkflowStatus.pending

        return WorkflowRecord(
            workflow_id=str(task.id),
            objective=task.original_request,
            context={"tenant_id": task.tenant_id},
            stages=[WorkflowStage.supervisor, WorkflowStage.planner, WorkflowStage.executor, WorkflowStage.reviewer],
            status=status
        )

_workflow_service = PostgresWorkflowService()

def get_workflow_service() -> PostgresWorkflowService:
    return _workflow_service

