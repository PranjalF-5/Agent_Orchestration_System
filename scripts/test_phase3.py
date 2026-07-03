import os
import uuid
import asyncio

# Set env vars for LiteLLM if needed, though they should be in .env
from agent_orchestration_system.core.config import get_settings
from agent_orchestration_system.orchestration.graph import app as graph_app
from agent_orchestration_system.memory.qdrant_setup import save_episodic_memory, search_similar_tasks
from langchain_core.messages import HumanMessage

def test_phase3():
    tenant_id = "test_tenant_phase3"
    task_id = str(uuid.uuid4())
    objective = "Analyze the performance of Agent Orchestration System."
    
    print(f"Testing Phase 3 for task: {task_id}")
    
    # 1. Run Graph
    initial_state = {
        "objective": objective,
        "messages": [HumanMessage(content=objective)],
        "sender": "user",
        "tenant_id": tenant_id
    }
    
    config = {"configurable": {"thread_id": task_id}}
    
    print("Executing Graph...")
    try:
        final_state = graph_app.invoke(initial_state, config=config)
        print("Graph execution completed successfully.")
        
        plan = final_state.get('plan', 'No plan generated')
        final_result = final_state['messages'][-1].content if final_state.get('messages') else ""
        
        print("\n--- Generated Plan ---")
        print(plan)
        print("\n--- Final Result ---")
        print(final_result)
        
        # 2. Save Episodic Memory
        print("\nSaving Episodic Memory to Qdrant...")
        save_episodic_memory(
            tenant_id=tenant_id,
            task_id=task_id,
            objective=objective,
            plan=plan,
            final_result=final_result
        )
        print("Memory saved successfully.")
        
        # 3. Search Similar Tasks
        print("\nSearching Qdrant for similar tasks...")
        results = search_similar_tasks(tenant_id, objective, limit=1)
        print(f"Search results: {results}")
        
    except Exception as e:
        print(f"Error during Phase 3 testing: {e}")

if __name__ == "__main__":
    test_phase3()
