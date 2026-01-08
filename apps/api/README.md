<!-- SSOT Domain: api -->
# Swarm Console API

The API is the control plane for swarm-console. It manages:

- **Repo selection** (single source of truth stored in `runtime/ssot/active_repo.json`)
- **Agent roster** (stored in `runtime/agents/agents.json`)
- **Task runs** (structured run records in `runtime/runs/`)
- **Evidence bundles** (command log, git diff, test output, files changed)
- **Outputs** (patch exports, optional git commit)

## How it works (data flow)

1. **Open repo** → `POST /open_repo_path` persists the repo path in `runtime/ssot/active_repo.json`.
2. **Create agents** → `POST /agents` stores the roster in `runtime/agents/agents.json`.
3. **Run task** → `POST /tasks/run` writes a run record:
   - `runtime/runs/<run_id>.json` (structured record)
   - `runtime/runs/<run_id>.patch` (git diff export)
   - `runtime/runs/<run_id>.summary.md` (human summary)
4. **Inspect evidence** → `GET /runs`, `GET /runs/{run_id}`, `GET /runs/{run_id}/summary`, `GET /runs/{run_id}/patch`.
5. **Optional commit** → `POST /runs/{run_id}/commit` to write a git commit inside the repo.

## Local setup

### 1) Install dependencies

```bash
python -m pip install fastapi uvicorn pydantic
```

### 2) Start the API

```bash
../../scripts/run_swarm_console_api.sh
```

The service listens on `http://localhost:8080`.

## Minimal walkthrough (CLI)

```bash
# 1) Open the repo (SSOT)
curl -X POST http://localhost:8080/open_repo_path \
  -H "Content-Type: application/json" \
  -d '{"path": "/path/to/repo"}'

# 2) Create agents
curl -X POST http://localhost:8080/agents \
  -H "Content-Type: application/json" \
  -d '{
    "agents": [
      {"id": "agent-1", "role": "repo-scaffold", "task": "Scaffold project"}
    ]
  }'

# 3) Run a task
curl -X POST http://localhost:8080/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain the repo structure"}'

# 4) List runs and inspect evidence
curl http://localhost:8080/runs
curl http://localhost:8080/runs/<run_id>
curl http://localhost:8080/runs/<run_id>/summary
curl http://localhost:8080/runs/<run_id>/patch
```

## Evidence bundle contents

Each run record includes:

- `command_log`: dispatch → execute → evidence → result markers
- `git_diff`: `git diff` output for the repo (if available)
- `test_output`: placeholder string (update to real tests later)
- `files_changed`: list from `git status --porcelain`

## Troubleshooting

- **Repo not found**: ensure the path exists and is accessible.
- **No git diff**: the repo may have no changes yet.
- **Commit fails**: ensure the repo has staged changes and a clean git config.

## Tutorial

For a guided, end-to-end walkthrough (UI + API), see:
`/docs/swarm-console/TUTORIAL.md`.
