from langgraph.graph import END, StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from agent_orchestration_system.core.config import get_settings
from agent_orchestration_system.orchestration.state import AgentState
from agent_orchestration_system.orchestration.agents.supervisor import supervisor_node
from agent_orchestration_system.orchestration.agents.planner import planner_node
from agent_orchestration_system.orchestration.agents.executor import executor_node

settings = get_settings()

def router(state: AgentState):
    # The supervisor's decision is in the last message
    if not state.get("messages"):
        return "planner"
    
    last_message = state["messages"][-1].content.strip().lower()
    
    if "planner" in last_message:
        return "planner"
    elif "executor" in last_message:
        return "executor"
    elif "finish" in last_message:
        return END
    
    # Default fallback
    return END

# Define the StateGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)

# Set entry point
workflow.set_entry_point("supervisor")

# Add edges
workflow.add_conditional_edges(
    "supervisor",
    router,
    {
        "planner": "planner",
        "executor": "executor",
        END: END
    }
)
workflow.add_edge("planner", "supervisor")
workflow.add_edge("executor", "supervisor")

# Setup PostgreSQL Checkpointer (Memory)
# We use a global pool for the application
db_url = settings.postgres_url.replace("+psycopg", "") # psycopg_pool expects pure postgresql://
connection_pool = ConnectionPool(conninfo=db_url, kwargs={"autocommit": True})
connection_pool.open()

# We need to initialize the tables once. Let's do it eagerly here for simplicity.
# In a real app, this might be done during startup.
checkpointer = PostgresSaver(connection_pool)
checkpointer.setup()
    
# Compile the graph with the checkpointer
app = workflow.compile(checkpointer=checkpointer)
