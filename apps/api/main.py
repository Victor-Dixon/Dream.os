# SSOT Domain: api
"""Swarm-console API scaffold for control plane operations."""
from __future__ import annotations

import json
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = REPO_ROOT / "runtime"
RUNS_DIR = RUNTIME_DIR / "runs"
AGENTS_DIR = RUNTIME_DIR / "agents"
LOGS_DIR = RUNTIME_DIR / "logs"
SSOT_DIR = RUNTIME_DIR / "ssot"
CONFIG_DIR = REPO_ROOT / "config"

PROVIDERS_CONFIG = CONFIG_DIR / "providers.json"
TOOLS_CONFIG = CONFIG_DIR / "tools.json"
ACTIVE_REPO_FILE = SSOT_DIR / "active_repo.json"
AGENTS_FILE = AGENTS_DIR / "agents.json"

app = FastAPI(title="swarm-console", version="0.1.0")


class RepoRequest(BaseModel):
    path: str = Field(..., description="Filesystem path to the repo to open.")


class AgentSpec(BaseModel):
    id: str
    role: str
    task: str


class CreateAgentsRequest(BaseModel):
    agents: List[AgentSpec] = Field(..., min_items=1, max_items=8)


class TaskRequest(BaseModel):
    repo_path: Optional[str] = None
    prompt: str
    agents: Optional[List[str]] = None


class TaskResponse(BaseModel):
    run_id: str
    status: str
    summary: str


class CommitRequest(BaseModel):
    message: str = Field(..., description="Commit message for optional Git commit.")


def _ensure_dirs() -> None:
    for directory in (RUNS_DIR, AGENTS_DIR, LOGS_DIR, SSOT_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _timestamp() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _run_command(command: List[str], cwd: Optional[Path] = None) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return "".join(command) + " (command not available)"
    output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    return output.strip()


def _collect_git_diff(repo_path: Optional[Path]) -> str:
    if not repo_path or not repo_path.exists():
        return ""
    return _run_command(["git", "-C", str(repo_path), "diff"])


def _collect_files_changed(repo_path: Optional[Path]) -> List[str]:
    if not repo_path or not repo_path.exists():
        return []
    status = _run_command(["git", "-C", str(repo_path), "status", "--porcelain"])
    files = []
    for line in status.splitlines():
        parts = line.strip().split(maxsplit=1)
        if len(parts) == 2:
            files.append(parts[1])
    return files


def _load_agents() -> List[Dict[str, Any]]:
    return _read_json(AGENTS_FILE, [])


def _load_active_repo(requested_path: Optional[str]) -> Optional[Path]:
    if requested_path:
        return Path(requested_path).expanduser()
    stored = _read_json(ACTIVE_REPO_FILE, {})
    if stored.get("path"):
        return Path(stored["path"]).expanduser()
    return None


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok", "time": _timestamp()}


@app.get("/config/providers")
async def providers_config() -> Dict[str, Any]:
    return _read_json(PROVIDERS_CONFIG, {})


@app.get("/config/tools")
async def tools_config() -> Dict[str, Any]:
    return _read_json(TOOLS_CONFIG, {})


@app.post("/open_repo_path")
async def open_repo_path(payload: RepoRequest) -> Dict[str, Any]:
    _ensure_dirs()
    repo_path = Path(payload.path).expanduser()
    if not repo_path.exists():
        raise HTTPException(status_code=404, detail="Repository path not found")
    record = {"path": str(repo_path), "opened_at": _timestamp()}
    _write_json(ACTIVE_REPO_FILE, record)
    return {"status": "ok", "repo": record}


@app.post("/agents")
async def create_agents(payload: CreateAgentsRequest) -> Dict[str, Any]:
    _ensure_dirs()
    if len(payload.agents) < 1 or len(payload.agents) > 8:
        raise HTTPException(status_code=400, detail="Agent count must be between 1 and 8")
    agents_data = [agent.model_dump() for agent in payload.agents]
    _write_json(AGENTS_FILE, agents_data)
    return {"status": "ok", "agents": agents_data}


@app.post("/tasks/run", response_model=TaskResponse)
async def run_task(payload: TaskRequest) -> TaskResponse:
    _ensure_dirs()
    repo_path = _load_active_repo(payload.repo_path)
    run_id = str(uuid.uuid4())
    dispatch_time = _timestamp()
    command_log = [
        f"dispatch::{dispatch_time}",
        f"execute::{_timestamp()}",
        f"evidence::{_timestamp()}",
        f"result::{_timestamp()}",
    ]
    git_diff = _collect_git_diff(repo_path)
    files_changed = _collect_files_changed(repo_path)
    test_output = "tests not run"
    summary = "Run completed with scaffolded outputs."

    run_record = {
        "id": run_id,
        "prompt": payload.prompt,
        "repo_path": str(repo_path) if repo_path else None,
        "agents": payload.agents or [agent["id"] for agent in _load_agents()],
        "status": "completed",
        "timestamps": {
            "dispatch": dispatch_time,
            "execute": _timestamp(),
            "evidence": _timestamp(),
            "result": _timestamp(),
        },
        "evidence_bundle": {
            "command_log": command_log,
            "git_diff": git_diff,
            "test_output": test_output,
            "files_changed": files_changed,
        },
        "outputs": {
            "patch_export": str((RUNS_DIR / f"{run_id}.patch").resolve()),
            "optional_git_commit": None,
        },
        "summary": summary,
    }

    _write_json(RUNS_DIR / f"{run_id}.json", run_record)
    (RUNS_DIR / f"{run_id}.patch").write_text(git_diff, encoding="utf-8")
    (RUNS_DIR / f"{run_id}.summary.md").write_text(
        f"# Run {run_id}\n\n{summary}\n", encoding="utf-8"
    )
    return TaskResponse(run_id=run_id, status="completed", summary=summary)


@app.get("/runs")
async def list_runs() -> Dict[str, Any]:
    _ensure_dirs()
    runs = sorted(RUNS_DIR.glob("*.json"))
    return {"runs": [path.stem for path in runs]}


@app.get("/runs/{run_id}")
async def get_run(run_id: str) -> Dict[str, Any]:
    run_file = RUNS_DIR / f"{run_id}.json"
    if not run_file.exists():
        raise HTTPException(status_code=404, detail="Run not found")
    return _read_json(run_file, {})


@app.get("/runs/{run_id}/summary")
async def get_run_summary(run_id: str) -> Dict[str, Any]:
    summary_file = RUNS_DIR / f"{run_id}.summary.md"
    if not summary_file.exists():
        raise HTTPException(status_code=404, detail="Summary not found")
    return {"summary": summary_file.read_text(encoding="utf-8")}


@app.get("/runs/{run_id}/patch")
async def get_run_patch(run_id: str) -> Dict[str, Any]:
    patch_file = RUNS_DIR / f"{run_id}.patch"
    if not patch_file.exists():
        raise HTTPException(status_code=404, detail="Patch not found")
    return {"patch": patch_file.read_text(encoding="utf-8")}


@app.post("/runs/{run_id}/commit")
async def commit_run(run_id: str, payload: CommitRequest) -> Dict[str, Any]:
    run_file = RUNS_DIR / f"{run_id}.json"
    if not run_file.exists():
        raise HTTPException(status_code=404, detail="Run not found")
    run_record = _read_json(run_file, {})
    repo_path = run_record.get("repo_path")
    if not repo_path:
        raise HTTPException(status_code=400, detail="Run has no repo_path")
    commit_output = _run_command(
        ["git", "-C", repo_path, "commit", "-am", payload.message]
    )
    run_record["outputs"]["optional_git_commit"] = payload.message
    _write_json(run_file, run_record)
    return {"status": "ok", "output": commit_output}
