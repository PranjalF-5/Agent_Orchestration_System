from agent_orchestration_system.orchestration.state import AgentState
from agent_orchestration_system.orchestration.agents.executor import executor_node

# Create a mock state with a plan that requires calculation
mock_state = AgentState(
    tenant_id="test_tenant_phase4",
    task_id="test_task_002",
    objective="Find current information.",
    plan="Search the web for the latest major news about AI in 2026 and summarize it briefly.",
    messages=[],
    sender="planner"
)

print("Executing Phase 4 test...")
result_state = executor_node(mock_state)

print("\n--- Final Executor Output ---")
for message in result_state.get("messages", []):
    print(message.content)
