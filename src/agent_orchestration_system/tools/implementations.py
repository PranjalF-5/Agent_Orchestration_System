from duckduckgo_search import DDGS
from agent_orchestration_system.tools.registry import registry, ToolDefinition

def web_search(query: str, max_results: int = 3) -> list[dict]:
    """Search the web using DuckDuckGo."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        return results

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        # Very basic safe eval using python's compile built-in with no globals/locals
        # In a real production system, use a proper sandboxed evaluator (like sympy or ast.literal_eval)
        # For MVP, eval with restricted globals is sufficient for basic math
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
        code = compile(expression, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise NameError(f"Use of name '{name}' is not allowed")
        
        result = eval(code, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# Register web_search
registry.register_tool(
    definition=ToolDefinition(
        name="web_search",
        description="Search the web for current information. Returns a list of snippets and URLs.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return. Default is 3."
                }
            },
            "required": ["query"]
        },
        cache_ttl_seconds=300 # Cache for 5 minutes
    ),
    func=web_search
)

# Register calculator
registry.register_tool(
    definition=ToolDefinition(
        name="calculator",
        description="Evaluates a mathematical expression (e.g., '2 + 2 * 5').",
        input_schema={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate."
                }
            },
            "required": ["expression"]
        },
        cache_ttl_seconds=None # Fast enough, no cache needed
    ),
    func=calculator
)
