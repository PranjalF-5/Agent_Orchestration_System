from litellm import completion
from langchain_core.messages import AIMessage
from agent_orchestration_system.orchestration.state import AgentState

def planner_node(state: AgentState):
    """
    Planner Agent: Creates a step-by-step plan.
    """
    print("---PLANNER---")
    
    prompt = f"""
    You are the Planner. The objective is: {state['objective']}.
    Please provide a concise, step-by-step plan to achieve this objective.
    """
    
    response = completion(
        model="nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )
    
    plan_text = response.choices[0].message.content.strip()
    print(f"Planner output: {plan_text}")
    
    return {"sender": "planner", "plan": plan_text, "messages": [AIMessage(content=plan_text)]}
