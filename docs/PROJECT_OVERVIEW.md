# Agent Orchestration System — Project Overview

Purpose
- Minimal Phase‑1 scaffold for a production‑grade multi‑agent orchestration platform.

High level architecture
- API layer: FastAPI app exposes HTTP endpoints and will host agent orchestration APIs.
- Orchestration: Phase 2 will introduce a coordinator (LangGraph or custom) to manage Supervisor → Planner → Executor → Reviewer flows.
- State & memory: short‑term state in Redis, durable records in PostgreSQL, long‑term memory via a vector DB (Chroma/Qdrant) behind an abstract interface.
- Tools & sandboxing: external tools invoked via a tool registry with sandboxing (gVisor/Firecracker) in production.

Tech stack (current)
- Python 3.12
- FastAPI (HTTP), Uvicorn (ASGI), Pydantic‑settings
- Tests: pytest, httpx
- Dev: Docker, docker‑compose

What is implemented
- FastAPI app factory (`create_app()`), entry point (`main.py`).
- Health routes: `/healthz`, `/readyz`.
- Configuration via `core/config.py` using pydantic‑settings.
- Editable project install (`pyproject.toml`) and dev extras for testing and linting.
- Basic tests under `tests/` and Dockerfile + docker‑compose for local integration.
- Phase 2 orchestration starter: in-memory workflow API under `/api/v1/workflows`.

Key files
- `src/agent_orchestration_system/main.py` — module-level `app` used by uvicorn.
- `src/agent_orchestration_system/app.py` — application factory and registration of routers/middleware.
- `src/agent_orchestration_system/core/config.py` — environment driven settings.
- `src/agent_orchestration_system/api/router.py` — API router composition.
- `src/agent_orchestration_system/api/routes/health.py` — health endpoints.

Next phases
1. Replace in-memory workflow storage with Redis/Postgres-backed workflow state.
2. Add task execution orchestration and agent handoff events.
3. Implement memory vector store and retrieval (abstract interface + adapter).
4. Tool registry, sandboxing, RBAC, and observability (OpenTelemetry).
5. Production packaging with Kubernetes & Helm, automated CI/CD.

Reference
- See `docs/DEV_SETUP.md` for local setup and run commands.
- See `docs/PHASE_2_ORCHESTRATION.md` for the workflow API and lifecycle.
