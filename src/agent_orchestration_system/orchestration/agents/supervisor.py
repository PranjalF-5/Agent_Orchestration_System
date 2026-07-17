from litellm import completion
from langchain_core.messages import AIMessage
from agent_orchestration_system.orchestration.state import AgentState
from agent_orchestration_system.memory.qdrant_setup import search_similar_tasks

def supervisor_node(state: AgentState):
    """
    Supervisor Agent: Decides the next step (Planner or Executor).
    """
    print("---SUPERVISOR---")
    
    # Retrieve past context from Qdrant
    tenant_id = state.get("tenant_id", "default_tenant")
    try:
        similar_tasks = search_similar_tasks(tenant_id, state['objective'], limit=2)
        past_context = "\n".join([f"- Objective: {t['objective']}\n  Plan: {t['plan']}" for t in similar_tasks])
    except Exception as e:
        print(f"Failed to query Qdrant: {e}")
        past_context = "No past context available."
    
    # Get recent messages to provide context of what has been done
    recent_messages = ""
    if state.get("messages"):
        # Take the last 3 messages, excluding the supervisor's own last decision
        for msg in state["messages"][-3:]:
            if msg.content not in ["planner", "executor"]:
                recent_messages += f"- {msg.content}\n"

    prompt = f"""
    You are the Supervisor. Your objective is: {state['objective']}.
    
    Based on the objective and the recent progress, what is the next step?
    - If there is NO plan, reply EXACTLY with the word 'planner'.
    - If there is a plan and the objective has NOT been fulfilled yet, reply EXACTLY with the word 'executor'.
    - If the tool outputs or recent progress show that the objective is completely fulfilled, reply EXACTLY with the word 'FINISH'. Do NOT output anything else!
    
    WARNING: The executor often completes multiple steps of the plan in a single tool call. If the final result you are looking for is present in the recent progress (e.g. the text you wanted to extract, or the result of a calculation), you MUST output 'FINISH' immediately. Do not keep calling executor.
    
    Current Plan: {state.get('plan', 'None')}
    
    Recent Progress/Results:
    {recent_messages if recent_messages else "None"}
    
    Relevant Past Experiences:
    {past_context}
    """
    
    response = completion(
        model="nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=50
    )
    
    decision = response.choices[0].message.content.strip().lower()
    print(f"Supervisor decision: {decision}")
    
    return {"sender": "supervisor", "messages": [AIMessage(content=decision)]}
