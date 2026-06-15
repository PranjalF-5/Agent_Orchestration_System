import pytest
from httpx import ASGITransport, AsyncClient
import uuid

from agent_orchestration_system.app import create_app

app = create_app()

@pytest.mark.anyio
async def test_create_task_endpoint():
    """Smoke test to ensure the POST /tasks endpoint returns 200 OK and correct schema."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "prompt": "Test task",
            "tenant_id": "test_tenant",
            "config": {}
        }
        response = await client.post("/tasks", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "pending"
