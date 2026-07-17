import sys
import os

# Add src to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from langchain_core.messages import HumanMessage
from agent_orchestration_system.orchestration.graph import app as graph_app
from uuid import uuid4

def main():
    thread_id = str(uuid4())
    print(f"Starting execution with thread_id: {thread_id}")
    
    objective = "Go to https://example.com and extract the exact text of the main heading (h1). Use browser_action."
    
    initial_state = {
        "objective": objective,
        "messages": [HumanMessage(content=objective)],
        "sender": "user",
        "tenant_id": "test_script_user"
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    
    final_state = graph_app.invoke(initial_state, config=config)
    
    print("\n\n--- FINAL RESULT ---")
    for msg in final_state.get("messages", []):
        print(f"[{msg.type}]: {msg.content}")
        
if __name__ == "__main__":
    main()
