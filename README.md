# Agent Orchestration System

Production-grade multi-agent platform inspired by the 2026 build guide.

## Phase 1 foundation

This repository starts with the smallest useful slice:

- FastAPI app factory and health endpoints
- typed environment settings
- Docker and Compose scaffolding
- source layout for later orchestration, memory, tool, HITL, and observability layers

## Local development

```bash
python -m uvicorn agent_orchestration_system.main:app --reload --app-dir src
```

## Next implementation phases

1. LangGraph orchestration engine
2. Redis short-term task state
3. PostgreSQL-backed durable workflow records
4. Tool registry, sandboxing, and logging
5. HITL queue and reviewer flow
6. OpenTelemetry traces and metrics
