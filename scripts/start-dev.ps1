<#
Start-dev.ps1
PowerShell helper to create & activate virtualenv, install dev dependencies if missing,
and start the FastAPI dev server with uvicorn.

Usage (PowerShell):
  .\scripts\start-dev.ps1            # create venv if needed, install if uvicorn missing, start on port 8000
  .\scripts\start-dev.ps1 -Port 9000 -Install:$false
#>

param(
    [int]$Port = 8000,
    [bool]$Install = $true
)

# Resolve the repository root from the script location.
$scriptDir = $PSScriptRoot
if (-not $scriptDir) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
}
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "Project root: $projectRoot"

# Create venv if missing
$venvPath = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment (.venv)..."
    py -3 -m venv $venvPath
}

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Error "Activation script not found at $activateScript"
    exit 1
}

# Allow running activation in this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force | Out-Null

Write-Host "Activating virtualenv..."
. $activateScript

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip | Out-Null

if ($Install) {
    # Install only if uvicorn (as a proxy for dev deps) is missing
    $uv = & python -m pip show uvicorn 2>$null
    if (-not $uv) {
        Write-Host "Installing project (editable) and dev dependencies... (this may take a minute)"
        python -m pip install -e .[dev]
    }
    else {
        Write-Host "Dev dependencies appear installed; skipping install."
    }
}

# Resolve python executable from venv and run uvicorn
$venvPython = Join-Path $venvPath "Scripts\python.exe"
if (Test-Path $venvPython) { $pythonCmd = $venvPython } else { $pythonCmd = "python" }

Write-Host "Starting uvicorn on http://127.0.0.1:$Port ... (press CTRL+C to stop)"
& $pythonCmd -m uvicorn agent_orchestration_system.main:app --reload --app-dir src --host 127.0.0.1 --port $Port --log-level info --access-log
