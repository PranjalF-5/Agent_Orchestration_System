from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from agent_orchestration_system.app import create_app
from agent_orchestration_system.orchestration.models import WorkflowCreateRequest
from agent_orchestration_system.orchestration.service import InMemoryWorkflowService


def test_create_workflow_returns_initial_orchestration_plan() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/workflows",
        json={
            "objective": "Summarize the weekly incident report",
            "context": {"tenant_id": "tenant-a", "source": "email"},
            "requested_by": "alice",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["objective"] == "Summarize the weekly incident report"
    assert body["status"] == "pending"
    assert body["stages"] == ["supervisor", "planner", "executor", "reviewer"]
    assert body["requested_by"] == "alice"


def test_get_created_workflow_returns_same_record() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/api/v1/workflows",
        json={"objective": "Draft a deployment checklist"},
    )
    workflow_id = create_response.json()["workflow_id"]

    get_response = client.get(f"/api/v1/workflows/{workflow_id}")

    assert get_response.status_code == 200
    assert get_response.json()["workflow_id"] == workflow_id


def test_missing_workflow_returns_404() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/workflows/missing-workflow-id")

    assert response.status_code == 404


def test_workflow_service_persists_between_instances(tmp_path: Path) -> None:
    storage_path = tmp_path / "workflows.json"

    service_a = InMemoryWorkflowService(storage_path=storage_path)
    created = service_a.create_workflow(
        WorkflowCreateRequest(objective="Keep workflow data after restart")
    )

    service_b = InMemoryWorkflowService(storage_path=storage_path)
    restored = service_b.get_workflow(created.workflow_id)

    assert restored.workflow_id == created.workflow_id
    assert restored.objective == "Keep workflow data after restart"
