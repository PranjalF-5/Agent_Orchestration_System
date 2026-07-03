from litellm import completion
from langchain_core.messages import AIMessage
from agent_orchestration_system.orchestration.state import AgentState

def executor_node(state: AgentState):
    """
    Executor Agent: Executes the plan.
    """
    print("---EXECUTOR---")
    
    prompt = f"""
    You are the Executor. The objective is: {state['objective']}.
    The plan is: {state.get('plan', 'No plan provided')}.
    
    Execute the plan and provide the final result.
    """
    
    response = completion(
        model="nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200
    )
    
    result = response.choices[0].message.content.strip()
    print(f"Executor output: {result}")
    
    return {"sender": "executor", "messages": [AIMessage(content=result)]}
