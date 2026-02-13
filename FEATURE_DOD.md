# FEATURE DOD (v1.0 closure audit)

This file defines **verifiable Definition of Done** targets per inventoried feature.
Each section includes:

- Acceptance tests (how to prove)
- Failure modes + exit codes
- Data/state contracts (DB/files/memory)
- Observability (logs/debug evidence)

---

## 01) Main service launcher and lifecycle control (`main.py`)

### Acceptance tests (how to prove)
- `python3 main.py --help` returns exit `0` and prints `Agent Cellphone V2 - Unified Service Launcher`.
- `python3 main.py --status` returns exit `0` and prints a structured service status summary (not unknown command).
- `python3 main.py --start --message-queue` returns non-zero on startup failure, zero on success.

### Failure modes + exit codes
- Invalid arg combinations (argparse): exit `2`.
- Unknown command mapping: exit `1`.
- Startup error in handler/service manager: exit `1`.
- User interrupt in foreground loop: graceful shutdown then exit `0`.

### Data/state contracts
- Reads/writes PID files under `pids/*.pid`.
- Writes service logs under `logs/*.log`.
- `ServiceManager.services` names must match handler-requested service names exactly.

### Observability
- Startup/stop/status actions print deterministic status lines.
- Failed service startup logs include service name and root cause.
- Health summary includes `running/total` counts.

---

## 02) Unified domain CLI + deprecated wrappers (`src.cli`, `src.core.cli`, `src.services.cli`)

### Acceptance tests (how to prove)
- `python3 -m src.cli --help` returns `0` and lists `services` and `core`.
- `python3 -m src.core.cli --help` returns `0` and routes to unified core domain.
- `python3 -m src.services.cli --help` returns `0` and routes to unified services domain.

### Failure modes + exit codes
- Missing domain/subcommand: exit `1`.
- Keyboard interrupt in unified router: exit `130`.
- Downstream command import failure: exit `1` with clear module name.

### Data/state contracts
- Wrapper CLIs must preserve original argv payload after domain prefixing.
- Domain router must not mutate global state beyond command dispatch.

### Observability
- Deprecation warnings should identify replacement command.
- Import failures include module path (for quick repair).

---

## 03) Packaged `agent-cellphone*` script entrypoints (`src/agent_cellphone/cli.py`)

### Acceptance tests (how to prove)
- `python3 src/agent_cellphone/cli.py --help` returns `0`.
- `agent-cellphone status` returns `0` and prints status block.
- `agent-cellphone coordinate --from Agent-1 --to Agent-2 --action ping` returns `0`.

### Failure modes + exit codes
- Parser errors/missing required flags: exit `2`.
- Runtime command error: exit `1`.
- Keyboard interrupt: exit `0` (as implemented) or documented alternative.

### Data/state contracts
- CLI does not mutate persistent state in "display-only" commands.
- Coordinate command payload schema: sender, recipient, action, optional message.

### Observability
- Command output must include command name, target agents, and result status.

---

## 04) Unified messaging CLI script (`messaging_cli_unified.py`)

### Acceptance tests (how to prove)
- `python3 messaging_cli_unified.py --help` returns `0`.
- `python3 messaging_cli_unified.py --agent Agent-1 --message "ping"` returns `0` on successful delivery path.
- `python3 messaging_cli_unified.py --broadcast --message "ops"` returns `0` if at least one recipient delivery succeeds.

### Failure modes + exit codes
- Missing required routing (`--agent` or `--broadcast`): exit `1`.
- Missing `--message` when required: exit `1`.
- Delivery dependency missing (e.g., pyautogui/pyperclip): exit `1` with explicit missing dependency text.

### Data/state contracts
- Message object includes `message_id`, sender, recipient(s), type, priority, tags.
- Devlog delivery writes JSONL entries; workspace delivery writes structured JSON.
- Soft-onboarding path consumes template and inserts agent-specific values.

### Observability
- Output includes recipient(s), message metadata, and per-method delivery status.
- Failure output includes method-specific errors.

---

## 05) Messaging service layer (`src/services/messaging_infrastructure.py`, `unified_messaging_service.py`)

### Acceptance tests (how to prove)
- Unit tests importing these modules can call public methods documented in test suite without attribute errors.
- `send_message()` returns stable schema: `{success: bool, ...}` with error context on failure.
- Broadcast path returns per-recipient status map or documented result envelope.

### Failure modes + exit codes
- Invalid destination/message payload: deterministic error object; CLI caller exits `1`.
- Queue unavailable: explicit degraded-mode or hard-fail contract (must be documented).

### Data/state contracts
- Service contracts must match existing tests and callers (message schema, queue_id semantics).
- No hidden global mutable state outside documented singleton/queue objects.

### Observability
- Structured logs for enqueue, delivery, block/validation outcomes.

---

## 06) Status CLI (`src/services/status_cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.services.status_cli --health` returns `0`.
- `python3 -m src.services.status_cli --agents` returns `0`.
- `python3 -m src.services.status_cli --coordination` returns `0`.
- `python3 -m src.services.status_cli --all` returns `0`.

### Failure modes + exit codes
- Internal exception in checks: exit `1`.
- No args/help path: exit `0` with usage text.

### Data/state contracts
- Reads `agent_workspaces/*`, optional `message_queue/`, optional `coordination_cache.json`.
- No write side effects for read-only status commands.

### Observability
- Output sections are deterministic: health, agents, coordination.
- Status severity mapping (`healthy/warning/critical`) visible in output.

---

## 07) Safety foundation CLI (`src/core/safety/cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.core.safety.cli status` returns `0` and prints component statuses.
- `python3 -m src.core.safety.cli sandbox --code "print(1)"` returns `0` and shows execution result.
- `python3 -m src.core.safety.cli snapshot --create` returns `0` and prints snapshot ID.

### Failure modes + exit codes
- Missing command/subcommand args: exit `2`.
- Safety component runtime exception: exit `1`.
- Unknown command: exit `1`.

### Data/state contracts
- Snapshot operations persist snapshot metadata/files via snapshot manager.
- Audit queries must not mutate audit history.
- Kill-switch actions mutate kill-switch state with authorization contract.

### Observability
- CLI output includes per-component state and integrity checks.
- Audit queries include timestamped event records.

---

## 08) Workflow CLI (`src/workflows/cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.workflows.cli create --name wf1 --type autonomous --goal "x"` returns `0` and writes workflow state file.
- `python3 -m src.workflows.cli list` returns `0` and lists created workflow.
- `python3 -m src.workflows.cli execute --name wf1` returns `0` for valid state.

### Failure modes + exit codes
- Missing required flags: exit `1` (or argparse `2` where parser-enforced).
- Invalid JSON for `--branches`: exit `1`.
- Missing workflow state file on execute: exit `1`.

### Data/state contracts
- Workflow state persisted in `workflow_states/*.json`.
- State restore must preserve step list and execution metadata.

### Observability
- Create/execute output includes workflow name and step counts.
- Restore warnings are explicit and non-silent.

---

## 09) Vision CLI (`src/vision/cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.vision.cli info` returns `0` and lists capability booleans.
- `python3 -m src.vision.cli capture --output out.png` returns `0` and writes image+json outputs.
- `python3 -m src.vision.cli ocr --input sample.png --output ocr.json` returns `0`.

### Failure modes + exit codes
- Missing required args (`ocr/analyze input`): argparse exit `2`.
- Capture/analysis runtime error: exit `1`.
- Keyboard interrupt in monitor mode: exit `0`.

### Data/state contracts
- Capture writes specified output image and adjacent analysis JSON.
- OCR/analyze output JSON schema includes extracted text or analysis metrics.

### Observability
- Output prints capture success, OCR region counts, UI element counts.

---

## 10) Overnight orchestrator CLI (`src/orchestrators/overnight/cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.orchestrators.overnight.cli status` returns `0`.
- `python3 -m src.orchestrators.overnight.cli start --cycles 1 --interval 1` starts and exits cleanly in controlled test.
- `python3 -m src.orchestrators.overnight.cli tasks --action list` returns scheduler status.

### Failure modes + exit codes
- Missing task args for add action: exit `1`.
- Runtime startup/monitor errors: exit `1`.
- Keyboard interrupt in monitor/start loops: exit `0`.

### Data/state contracts
- Scheduler state must preserve task IDs, status, and retry counters.
- Recovery status reflects persisted failure history.

### Observability
- Start/status/monitor output includes cycle/task counters and timestamps.

---

## 11) Trader replay CLI (`src/services/trader_replay/trader_replay_cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.services.trader_replay.trader_replay_cli --help` returns `0`.
- Full smoke workflow returns expected exits:
  - `create` -> `0`
  - `start` -> `0`
  - `step` -> `0`
  - `pause` -> `0`
  - `status` -> `0` for existing session, `1` for missing session

### Failure modes + exit codes
- Missing parser-required args: exit `2`.
- Session not found: exit `1`.
- Orchestrator initialization failure: exit `1`.

### Data/state contracts
- Session persistence in configured SQLite db path.
- Replay state contract includes `current_index`, `total_candles`, `progress`.

### Observability
- Each command prints session ID and action result.
- Errors include clear reason text.

---

## 12) TSLA report CLI (`src/trading_robot/tsla_report/cli/tsla_report_cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.trading_robot.tsla_report.cli.tsla_report_cli morning_report --dry-run` returns `0` and prints payload output.
- `score_recommendations --date YYYY-MM-DD` returns `0` and prints JSON array.
- `weekly_summary` returns `0` and prints JSON summary.

### Failure modes + exit codes
- Missing command/subcommand args: argparse `2`.
- Missing publisher/import/dependency error: exit `1`.
- Discord post failure in non-dry mode: non-zero exit with reason.

### Data/state contracts
- Writes ledger rows for snapshots/recommendations/scores.
- Archives report artifacts under devlog/report paths.
- Snapshot hash integrity preserved across saved recommendation rows.

### Observability
- Command output includes command result, publish status, and persisted artifact paths.

---

## 13) OSS contribution CLI (`src/opensource/oss_cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.opensource.oss_cli --help` returns `0`.
- `list` returns `0` and prints project inventory.
- `status` returns `0` and prints aggregate metrics.

### Failure modes + exit codes
- Missing required args (`clone url`, `issues project_id`, `pr fields`): argparse `2`.
- project not found in `issues`: exit `1`.
- runtime operation error: exit `1`.

### Data/state contracts
- Project registry persists IDs/metadata.
- Imported issues map to task records with stable IDs.

### Observability
- Outputs include project counts, PR metrics, and command-specific summaries.

---

## 14) ChatGPT integration CLI (`src/services/chatgpt/cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.services.chatgpt.cli info` returns `0`.
- `send --message "hello" --wait` returns `0` when browser/session available.
- `extract --url <conversation> --output conv.json` returns `0` and writes file.

### Failure modes + exit codes
- Missing required args: argparse `2`.
- navigation/session/extraction runtime failures: exit `1`.
- Keyboard interrupt: exit `0`.

### Data/state contracts
- Saved conversation file includes id/url/message_count/messages.
- Session actions (`load/clear/info`) mutate/read browser-session state consistently.

### Observability
- Output includes navigation status, response wait status, extraction counts, save paths.

---

## 15) Analytics readiness CLI (`src/tools/analytics_readiness_cli.py`)

### Acceptance tests (how to prove)
- `python3 -m src.tools.analytics_readiness_cli --check-sites` returns `0`.
- `--check-configs` returns `0` with per-site check output.
- `--validate-ids` returns `0` with ID validation summary.
- `--full-report` returns `0` with readiness score and summary.

### Failure modes + exit codes
- Syntax/parser/runtime errors: exit `1`.
- No action flags: exit `0` after help (as currently designed) or documented alternative.

### Data/state contracts
- Reads under `websites/*/wp-config-analytics.php`.
- Read-only operations; no writes expected.

### Observability
- Output includes per-site pass/fail and aggregated readiness score.

---

## 16) System discovery agent CLI (`src/tools/system_discovery_agent.py`)

### Acceptance tests (how to prove)
- `python3 -m src.tools.system_discovery_agent --search "analysis"` returns `0`.
- `--recommend --task "code review"` returns `0` and ranked recommendations.
- `--learn --system swarm_coordinator` returns `0` and full metadata.
- `--training --role integration_coordinator` returns `0` and ordered training plan.

### Failure modes + exit codes
- Malformed/missing option combos: exit `2` (argparse) or `1` for semantic errors.
- Unknown system key in `--learn`: exit `0` with not-found notice (or documented non-zero policy).

### Data/state contracts
- Registry and usage history are in-memory structures unless explicit persistence is added.
- Recommendation ranking uses deterministic score function over capability/context fields.

### Observability
- Output includes relevance scores, recommendation reasons, and training priorities.

---

## 17) Risk analytics service/API modules

### Acceptance tests (how to prove)
- `python3 -m src.services.risk_analytics.risk_api_endpoints` returns `0` and prints comprehensive metrics JSON.
- `python3 -m src.services.risk_analytics.risk_calculator_service` returns `0` and prints risk metric report.
- Unit tests for endpoint and calculator modules pass in CI environment.

### Failure modes + exit codes
- Input validation failure (missing `user_id`/returns): structured error payload with status `error`.
- Unexpected calculation exception: structured error payload and logged exception.

### Data/state contracts
- Metrics payload schema stable: var/cvar/sharpe/drawdown/calmar/sortino/information.
- `calculate_risk_metrics` POST contract includes `returns_data` and optional equity/benchmark series.

### Observability
- Logs identify metric calculation failures by endpoint/operation.
- Outputs include metric names and calculation timestamps.

---

## 18) Unified persistence infrastructure

### Acceptance tests (how to prove)
- `python3 -m src.infrastructure.unified_persistence` returns `0` in a configured environment.
- CRUD operations through `UnifiedPersistenceService` work for agent/task repositories.
- `get_database_stats`, `backup_database`, `optimize_database` return deterministic success/failure values.

### Failure modes + exit codes
- DB path inaccessible: module/CLI wrapper returns non-zero.
- backup source missing: returns false with explicit message.

### Data/state contracts
- SQLite-backed schema via persistence repository modules.
- backup creates a filesystem copy preserving DB bytes.

### Observability
- Logs for optimization/backup success/failure.
- stats output includes row/entity counts.

---

## 19) Unified browser infrastructure service

### Acceptance tests (how to prove)
- `python3 -m src.infrastructure.unified_browser_service` returns `0` in complete environment.
- `start_browser` + `create_session` + `navigate_to_conversation` + `send_message` follow documented bool-return contracts.

### Failure modes + exit codes
- Browser adapter startup failure: non-zero in executable wrapper or false return in API.
- Missing driver/session preconditions: explicit false return + reason where applicable.

### Data/state contracts
- Cookie manager persists per-service cookies to configured cookie file.
- Session manager tracks request-rate and session metadata.

### Observability
- `get_browser_info` provides current URL/title/session counts.
- Request-rate decisions are inspectable through status methods.

---

## 20) Swarm brain knowledge base

### Acceptance tests (how to prove)
- Add/search/filter flows pass using temporary `brain_root`.
- `knowledge_base.json` and category markdown files are created and updated.
- `search`, `get_by_agent`, `get_by_category` return deterministic lists.

### Failure modes + exit codes
- Corrupt KB JSON should raise/return controlled error path (not silent data loss).
- malformed entry records are skipped with warning (as implemented in search).

### Data/state contracts
- Canonical state in `knowledge_base.json`:
  - `entries` map
  - `stats.total_entries`
  - `stats.contributors`
- Category markdown append contract under `shared_learnings/`.

### Observability
- Logger confirms entry add operations and malformed-record skips.

---

## 21) Project scanner integration

### Acceptance tests (how to prove)
- `python3 -m src.core.project_scanner_integration --help` returns `0`.
- `scan` action produces scan metadata and result payload.
- cache/history commands read and summarize cached scan files.

### Failure modes + exit codes
- scanner import unavailable: command returns `1` with explicit scanner error.
- result file missing after scan: command returns `1`.
- Thea guidance unavailable: command still returns `0` with fallback guidance marker.

### Data/state contracts
- Cached scan JSON in `project_scans/*_scan_cache.json`.
- scan metadata fields: project path, timestamp, duration, cache flag.

### Observability
- scan output prints file counts and durations.
- guidance path includes source marker (`thea_integrated` vs fallback).

---

## Global closure gates for DoD completion

- All primary CLI entrypoints in inventory compile and run `--help` with expected exit codes.
- Compile-error count in `src/` is reduced from current 21 to 0.
- Dependency bootstrap is reproducible (`dotenv`, `pytest`, and runtime messaging/browser deps installed by documented setup path).
- For each feature above:
  - at least one deterministic acceptance test in CI
  - explicit exit-code contract documented
  - state contract documented
  - observable logging/output contract documented
