import json
from litellm import completion
from agent_orchestration_system.orchestration.state import AgentState

# Ensure tools are registered
import agent_orchestration_system.tools.implementations
from agent_orchestration_system.tools.registry import registry

def executor_node(state: AgentState) -> dict:
    """
    Executor agent is responsible for executing the specific subtask 
    assigned by the Planner using tools.
    """
    current_subtask = state["plan"]
    
    prompt = f"Execute this subtask: {current_subtask}\nUse the available tools if necessary."
    
    tool_schemas = registry.get_all_tool_schemas()
    
    messages = [
        {"role": "system", "content": "You are the Executor. You have access to tools. Use them to solve the subtask. If the task involves visiting a specific URL or clicking elements on a page, YOU MUST use the 'browser_action' tool and provide the URL and an optional CSS selector. Otherwise, use 'web_search' for general queries."},
        {"role": "user", "content": prompt}
    ]
    
    response = completion(
        model="nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        messages=messages,
        tools=tool_schemas,
        temperature=0.2,
        max_tokens=800
    )
    
    response_message = response.choices[0].message
    
    if hasattr(response_message, "tool_calls") and response_message.tool_calls:
        # Convert response_message to dict for litellm if needed, or pass directly
        messages.append(response_message)
        last_tool_result = ""
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            tool_result = registry.execute_tool(function_name, function_args)
            last_tool_result = str(tool_result)
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(tool_result),
            })
            
        second_response = completion(
            model="nvidia_nim/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
            messages=messages,
            tools=tool_schemas,
            temperature=0.2,
            max_tokens=800
        )
        content = second_response.choices[0].message.content
        if content:
            result = f"{content.strip()}\n\n[Tool Output: {last_tool_result}]"
        else:
            result = f"Tool {function_name} executed. Result: {last_tool_result}"
    else:
        result = response_message.content.strip() if response_message.content else "Executed."
    
    print(f"Executor output: {result}")
    
    from langchain_core.messages import AIMessage
    return {"sender": "executor", "messages": [AIMessage(content=result)]}
