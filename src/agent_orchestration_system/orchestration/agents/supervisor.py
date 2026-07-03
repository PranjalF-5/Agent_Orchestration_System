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
    
    prompt = f"""
    You are the Supervisor. Your objective is: {state['objective']}.
    
    Based on the objective, what is the next step?
    If we need a step-by-step plan, reply EXACTLY with the word 'planner'.
    If we have a plan and need to execute it, reply EXACTLY with the word 'executor'.
    If the objective is completely fulfilled, reply EXACTLY with the word 'FINISH'.
    
    Current Plan: {state.get('plan', 'None')}
    
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
