from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent_orchestration_system.core.config import get_settings
from agent_orchestration_system.api.routes import tasks

settings = get_settings()

app = FastAPI(
    title="Agent Orchestration System API",
    description="API for the Agent Orchestration System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all origins. In production, restrict to frontend domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(tasks.router)

@app.get("/health", tags=["system"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy"}
