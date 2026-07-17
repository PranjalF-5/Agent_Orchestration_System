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

import ctypes

def browser_action(url: str, css_selector: str = None) -> str:
    """Automate the browser using Playwright to extract content."""
    
    try:
        from playwright.sync_api import sync_playwright
        import time
        
        with sync_playwright() as p:
            # We launch headless=False as per user request
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            
            # Wait a bit for JS to render
            time.sleep(3)
            
            if css_selector:
                try:
                    locator = page.locator(css_selector).first
                    text = locator.inner_text()
                except Exception:
                    text = f"Could not find elements matching selector: {css_selector}"
            else:
                # If no selector, just get the body text
                text = page.locator("body").inner_text()
                
            browser.close()
            
            # Return first 2000 chars to avoid overwhelming the LLM
            return text[:2000] + "..." if len(text) > 2000 else text
            
    except Exception as e:
        return f"Error executing playwright script: {str(e)}"

# Register browser_action
registry.register_tool(
    definition=ToolDefinition(
        name="browser_action",
        description="Opens a browser, navigates to a URL, and extracts text. Optionally provide a CSS selector (e.g. 'h1' or 'p') to extract specific elements. If no selector is provided, extracts the whole page body.",
        input_schema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to navigate to."
                },
                "css_selector": {
                    "type": "string",
                    "description": "Optional CSS selector to extract specific text."
                }
            },
            "required": ["url"]
        },
        cache_ttl_seconds=None
    ),
    func=browser_action
)
