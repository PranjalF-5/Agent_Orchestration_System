# Phase 2 — Orchestration Starter

Goal
- Introduce the first working slice of the orchestration layer without depending on Redis, PostgreSQL, or external agent runtime.

Current behavior
- `POST /api/v1/workflows` creates a workflow record and persists it to `data/workflows.json`.
- `GET /api/v1/workflows` lists created workflows.
- `GET /api/v1/workflows/{workflow_id}` returns one workflow record or 404.

Workflow shape
- Objective: the work the system should accomplish.
- Context: arbitrary JSON metadata passed in at creation time.
- Stages: `supervisor`, `planner`, `executor`, `reviewer`.
- Status: `pending`, `running`, `completed`.

Implementation notes
- The service uses a small JSON file so workflow IDs survive restarts, while still being easy to replace later.
- The service lives under `src/agent_orchestration_system/orchestration/`.
- The API router is registered from `src/agent_orchestration_system/api/router.py`.

Example request

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/v1/workflows -ContentType 'application/json' -Body '{"objective":"Summarize the weekly incident report","context":{"tenant_id":"tenant-a"}}'
```

Planned replacement
- Swap the in-memory store for Redis/Postgres-backed state.
- Add workflow transitions, agent handoff events, and durability.
- If you want a clean slate, delete `data/workflows.json`.
