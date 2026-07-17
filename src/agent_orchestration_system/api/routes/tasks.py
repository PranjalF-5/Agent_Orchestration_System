from fastapi import APIRouter, status, HTTPException
import uuid

from agent_orchestration_system.api.schemas.tasks import TaskRequest, TaskResponse
from agent_orchestration_system.orchestration.service import get_workflow_service, WorkflowNotFoundError
from agent_orchestration_system.orchestration.models import WorkflowCreateRequest, WorkflowStatus
from agent_orchestration_system.orchestration.graph import app as graph_app
from langchain_core.messages import HumanMessage

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def create_task(request: TaskRequest) -> TaskResponse:
    # 1. Create task record in database
    service = get_workflow_service()
    workflow_request = WorkflowCreateRequest(
        objective=request.prompt,
        context={"tenant_id": request.tenant_id, **request.config}
    )
    workflow_record = service.create_workflow(workflow_request)
    
    # 2. Execute LangGraph synchronously
    initial_state = {
        "objective": request.prompt,
        "messages": [HumanMessage(content=request.prompt)],
        "sender": "user"
    }
    
    try:
        # Run graph
        # For checkpointer, we need to pass a thread_id in the config
        config = {"configurable": {"thread_id": workflow_record.workflow_id}}
        final_state = graph_app.invoke(initial_state, config=config)
        
        # Save to Qdrant (Long-Term Memory)
        from agent_orchestration_system.memory.qdrant_setup import save_episodic_memory
        plan = final_state.get('plan', 'No plan generated')
        
        # Extract the actual result, skipping supervisor routing decisions
        final_result = ""
        for msg in reversed(final_state.get('messages', [])):
            content = msg.content.strip()
            if content.lower() not in ["planner", "executor", "finish"]:
                final_result = content
                break
        save_episodic_memory(
            tenant_id=request.tenant_id,
            task_id=workflow_record.workflow_id,
            objective=request.prompt,
            plan=plan,
            final_result=final_result
        )
        
        # Update status
        service.update_workflow_status(workflow_record.workflow_id, WorkflowStatus.completed)
        return TaskResponse(
            task_id=uuid.UUID(workflow_record.workflow_id), 
            status="completed",
            result=final_result,
            plan=plan
        )
    except Exception as e:
        print(f"Graph execution failed: {e}")
        return TaskResponse(task_id=uuid.UUID(workflow_record.workflow_id), status="failed", result=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: uuid.UUID) -> TaskResponse:
    service = get_workflow_service()
    try:
        record = service.get_workflow(str(task_id))
        return TaskResponse(task_id=task_id, status=record.status.value)
    except WorkflowNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
