import json
from pathlib import Path
from uuid import uuid4

from agent_orchestration_system.orchestration.models import (
    WorkflowCreateRequest,
    WorkflowRecord,
    WorkflowStage,
    WorkflowStatus,
)


class WorkflowNotFoundError(KeyError):
    """Raised when a workflow id cannot be found."""


class InMemoryWorkflowService:
    def __init__(self, storage_path: Path | None = None) -> None:
        self._storage_path = storage_path or Path("data/workflows.json")
        self._workflows: dict[str, WorkflowRecord] = {}
        self._load_from_disk()

    def create_workflow(self, payload: WorkflowCreateRequest) -> WorkflowRecord:
        workflow_id = uuid4().hex
        record = WorkflowRecord(
            workflow_id=workflow_id,
            objective=payload.objective,
            context=dict(payload.context),
            requested_by=payload.requested_by,
            stages=[
                WorkflowStage.supervisor,
                WorkflowStage.planner,
                WorkflowStage.executor,
                WorkflowStage.reviewer,
            ],
            status=WorkflowStatus.pending,
        )
        self._workflows[workflow_id] = record
        self._save_to_disk()
        return record

    def get_workflow(self, workflow_id: str) -> WorkflowRecord:
        try:
            return self._workflows[workflow_id]
        except KeyError as exc:
            raise WorkflowNotFoundError(workflow_id) from exc

    def list_workflows(self) -> list[WorkflowRecord]:
        return list(self._workflows.values())

    def _load_from_disk(self) -> None:
        if not self._storage_path.exists():
            return

        raw_text = self._storage_path.read_text(encoding="utf-8")
        if not raw_text.strip():
            return

        raw_workflows = json.loads(raw_text)
        self._workflows = {
            workflow_id: WorkflowRecord.model_validate(workflow_data)
            for workflow_id, workflow_data in raw_workflows.items()
        }

    def _save_to_disk(self) -> None:
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        serializable_workflows = {
            workflow_id: workflow.model_dump(mode="json")
            for workflow_id, workflow in self._workflows.items()
        }
        self._storage_path.write_text(
            json.dumps(serializable_workflows, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


_workflow_service = InMemoryWorkflowService()


def get_workflow_service() -> InMemoryWorkflowService:
    return _workflow_service

