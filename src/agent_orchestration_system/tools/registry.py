import json
import redis
import hashlib
from typing import Dict, Any, Optional, Callable
from pydantic import BaseModel
from agent_orchestration_system.core.config import get_settings

settings = get_settings()

class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict
    requires_sandbox: bool = False
    requires_hitl: bool = False
    cache_ttl_seconds: Optional[int] = None

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.implementations: Dict[str, Callable] = {}
        
        # Sync Redis client for caching
        self.redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
        
    def register_tool(self, definition: ToolDefinition, func: Callable):
        self.tools[definition.name] = definition
        self.implementations[definition.name] = func
        
    def get_tool_definition(self, name: str) -> Optional[ToolDefinition]:
        return self.tools.get(name)

    def get_all_tool_schemas(self) -> list[dict]:
        """Returns schemas formatted for LiteLLM/OpenAI tool calling."""
        schemas = []
        for name, tool_def in self.tools.items():
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool_def.name,
                    "description": tool_def.description,
                    "parameters": tool_def.input_schema
                }
            })
        return schemas

    def execute_tool(self, name: str, kwargs: dict) -> Any:
        if name not in self.implementations:
            return f"Error: Tool '{name}' not found."
            
        tool_def = self.tools[name]
        func = self.implementations[name]
        
        # Simple Caching mechanism
        if tool_def.cache_ttl_seconds:
            # Create a deterministic hash for the input
            kwargs_str = json.dumps(kwargs, sort_keys=True)
            input_hash = hashlib.md5(f"{name}:{kwargs_str}".encode()).hexdigest()
            cache_key = f"tool_cache:{name}:{input_hash}"
            
            try:
                cached_result = self.redis_client.get(cache_key)
                if cached_result:
                    print(f"[ToolRegistry] Cache hit for {name}")
                    return cached_result
            except Exception as e:
                print(f"Redis cache error: {e}")
                
        # Execute the tool
        print(f"[ToolRegistry] Executing {name} with args: {kwargs}")
        try:
            result = func(**kwargs)
            
            # Save to cache
            if tool_def.cache_ttl_seconds:
                try:
                    # Convert result to string if it isn't
                    if not isinstance(result, str):
                        result = json.dumps(result)
                    self.redis_client.setex(cache_key, tool_def.cache_ttl_seconds, result)
                except Exception as e:
                    print(f"Redis cache error on save: {e}")
                    
            return result
        except Exception as e:
            return f"Error executing tool '{name}': {str(e)}"

# Global instance
registry = ToolRegistry()
