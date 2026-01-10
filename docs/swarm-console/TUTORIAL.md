<!-- SSOT Domain: documentation -->
# Swarm Console Tutorial

This tutorial walks through a complete, end-to-end run cycle using the API and UI.

## Prerequisites

- Python 3.10+
- A local git repository you can point to
- Ports 8080 (API) and 5173 (UI) available

## Step 1 — Start the API

```bash
cd /workspace/Dream.os
./scripts/run_swarm_console_api.sh
```

You should see `Uvicorn running on http://127.0.0.1:8080`.

## Step 2 — Start the UI

Open a new terminal and run:

```bash
cd /workspace/Dream.os
./scripts/run_swarm_console_ui.sh
```

Open `http://localhost:5173` in a browser.

## Step 3 — Open a repo (SSOT)

In the UI **Repo** panel:

1. Paste the repo path (example: `/workspace/Dream.os`).
2. Click **Open Repo**.

The API stores this in `runtime/ssot/active_repo.json` as the SSOT for the session.

## Step 4 — Create agents

In the **Agents** panel:

1. Update the JSON roster.
2. Click **Save Agents**.

The roster is stored in `runtime/agents/agents.json`.

## Step 5 — Run a task

In the **Task Runner** panel:

1. Enter a prompt (example: `Summarize the repo structure.`).
2. Click **Run Task**.

This generates a run record in `runtime/runs/`.

## Step 6 — Inspect runs and evidence

In **Runs & Logs**:

1. Click **Refresh Runs**.
2. Select a run ID.

You will see:

- `command_log` showing the task lifecycle
- `git_diff` output
- `test_output` placeholder
- `files_changed` list

## Step 7 — Export patch (optional)

Each run creates a patch export at:

```
runtime/runs/<run_id>.patch
```

You can share or apply this patch as needed.

## Step 8 — Commit changes (optional)

If you want the API to create a commit:

```bash
curl -X POST http://localhost:8080/runs/<run_id>/commit \
  -H "Content-Type: application/json" \
  -d '{"message": "feat: update via swarm-console"}'
```

## Tips for simplifying setup

- Keep the API and UI scripts in separate terminals.
- Use one repo path consistently so your SSOT stays stable.
- If you want to avoid CLI calls entirely, rely on the UI workflow above.

## Where to look for data

- `runtime/ssot/active_repo.json` → active repo path
- `runtime/agents/agents.json` → active agent roster
- `runtime/runs/*.json` → run records and evidence
- `runtime/runs/*.patch` → patch exports
- `runtime/runs/*.summary.md` → summaries
