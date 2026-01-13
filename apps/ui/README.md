<!-- SSOT Domain: ui -->
# Swarm Console UI

Static UI for interacting with the swarm-console API.

## Run locally

```bash
../../scripts/run_swarm_console_ui.sh
```

Open `http://localhost:5173` in a browser.

## How it works

The UI is a static client that calls the API:

- **Repo panel** → `POST /open_repo_path`
- **Agents panel** → `POST /agents`
- **Task Runner** → `POST /tasks/run`
- **Runs & Logs** → `GET /runs` and `GET /runs/{run_id}`

The UI expects the API to run at `http://localhost:8080`. Update
`apps/ui/app.js` if you need a different base URL.

## Recommended workflow

1. **Start the API**: `../../scripts/run_swarm_console_api.sh`
2. **Start the UI**: `../../scripts/run_swarm_console_ui.sh`
3. **Open repo**: paste the repo path and click **Open Repo**.
4. **Create agents**: edit the JSON roster and click **Save Agents**.
5. **Run task**: enter a prompt and click **Run Task**.
6. **Inspect evidence**: click **Refresh Runs** and select a run.

## Troubleshooting

- **“API not connected”**: ensure the API is running on port 8080.
- **Agents JSON error**: the roster must be valid JSON.
- **Runs list empty**: run a task first to create a run record.

## Tutorial

For a step-by-step walkthrough, see:
`/docs/swarm-console/TUTORIAL.md`.
