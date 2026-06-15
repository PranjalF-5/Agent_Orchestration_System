# Developer Setup & Run Instructions

Prerequisites
- Python 3.12 installed (use the `py -3` launcher on Windows).
- Docker & Docker Compose (optional for containerized runs).

Local development (recommended)
1. Create and activate a virtual environment (PowerShell):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Upgrade pip and install project (editable) with dev extras:

```powershell
py -3 -m pip install --upgrade pip
py -3 -m pip install -e .[dev]
```

3. Run tests:

```powershell
py -3 -m pytest -q
```

4. Start the dev server (reload watches files):

```powershell
py -3 -m uvicorn agent_orchestration_system.main:app --reload --app-dir src --host 127.0.0.1 --port 8000
```

5. Verify health:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/healthz | ConvertTo-Json -Compress
```

Common issues
- `No module named uvicorn`: Make sure venv is active or install deps into the environment. Use `py -3 -m uvicorn ...` to run a module directly.
- Scripts installed but not on PATH: this is normal when using the global Python; activate venv to avoid.
- Windows PowerShell activation blocked: run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force` then activate.

Docker (optional)
- Build & run the dev stack (api + deps):

```powershell
docker compose up --build
```

Stop and remove containers

```powershell
docker compose down
```

Where to look next
- `src/agent_orchestration_system/app.py` — app factory and router registration
- `src/agent_orchestration_system/core/config.py` — configuration pattern
- `tests/test_health.py` — example unit test pattern
