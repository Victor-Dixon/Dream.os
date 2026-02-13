# PROJECT INVENTORY (v1.0 closure audit)

## Audit scope and evidence

- Repo root audited: `/workspace`
- Requested paths checked: `src`, `dream_os`, `project_scanner`, `cli`, `agents`, `runtime`, `db`, `tests`
- Observed path drift:
  - Missing at repo root: `dream_os/`, `project_scanner/`, `agents/`, `runtime/`, `db/`
  - Effective code root is `src/`
- Static/Runtime evidence collected:
  - `python3` CLI smoke matrix over primary entrypoints (help + basic dispatch)
  - `py_compile` full pass over `src` (1223 Python files, 21 compile failures)
  - Dependency availability checks (`dotenv`, `pyautogui`, `pyperclip`, `pytest`)
  - Representative test-file presence mapping in `tests/`

### High-signal observations

- Compile failures: **21 files** (syntax/indentation/conflict-marker class failures)
- Import blocker: `dotenv` missing in environment; `src.core.__init__` transitively imports it, causing broad CLI/module failures
- Packaged CLI mismatch:
  - `pyproject.toml` declares `agent-cellphone*` scripts
  - `src/agent_cellphone/cli.py` is syntactically broken
- Consolidation drift:
  - `src/cli/commands/start_handler.py` (used by `main.py`) is broken (`result` used before assignment)
  - duplicate handler tree exists under `src/cli/commands/handlers/`
- Messaging drift:
  - `src.cli` routes `services messaging` to `src.services.messaging_cli` (module missing)
  - `src/services/messaging_infrastructure.py` and `src/services/unified_messaging_service.py` are minimal shims/stubs

---

## CLI entrypoint coverage checklist

Covered in inventory below:

- `cli:python3 main.py`
- `cli:python3 -m src.cli`
- `cli:python3 -m src.core.cli` (deprecated wrapper)
- `cli:python3 -m src.services.cli` (deprecated wrapper)
- `cli:python3 src/agent_cellphone/cli.py`
- `cli:python3 messaging_cli_unified.py`
- `cli:python3 -m src.core.safety.cli`
- `cli:python3 -m src.services.status_cli`
- `cli:python3 -m src.services.trader_replay.trader_replay_cli`
- `cli:python3 -m src.workflows.cli`
- `cli:python3 -m src.vision.cli`
- `cli:python3 -m src.orchestrators.overnight.cli`
- `cli:python3 -m src.trading_robot.tsla_report.cli.tsla_report_cli`
- `cli:python3 -m src.opensource.oss_cli`
- `cli:python3 -m src.services.chatgpt.cli`
- `cli:python3 -m src.tools.analytics_readiness_cli`
- `cli:python3 -m src.tools.system_discovery_agent`

Additional module entrypoints (non-CLI but executable):

- `module:python3 -m src.services.risk_analytics.risk_api_endpoints`
- `module:python3 -m src.services.risk_analytics.risk_calculator_service`
- `module:python3 -m src.infrastructure.unified_persistence`
- `module:python3 -m src.infrastructure.unified_browser_service`
- `module:python3 -m src.swarm_brain.knowledge_base`
- `module:python3 -m src.core.project_scanner_integration`

---

## feature_inventory

### Feature 01
- name: Main service launcher and service lifecycle control
- description: Root launcher (`main.py`) with argument parsing and service start/stop/status orchestration.
- status: broken
- entrypoints:
  - cli:python3 main.py --help
  - cli:python3 main.py --start --message-queue
  - cli:python3 main.py --status
- primary_files:
  - main.py
  - src/cli/argument_parser.py
  - src/services/service_manager.py
  - src/cli/commands/start_handler.py
  - src/cli/commands/status_handler.py
  - src/cli/commands/stop_handler.py
- dependencies:
  - stdlib argparse/subprocess/pathlib
  - scripts/start_message_queue.py
  - scripts/start_twitch.py
  - scripts/start_fastapi.py
  - tools/utilities/discord_bot_launcher.py
- tests:
  - existing: tests/standalone/test_main_integration.py
  - missing: direct tests for `main.py --status/--stop/--kill` dispatch and exit codes
- risks:
  - `main.py --status` returns unknown-command exit 1 (parser emits `status`, main does not route it)
  - `src/cli/commands/start_handler.py` uses `result` before assignment; runtime failure text shown
  - failure path still exits code 0 in some start flows (operational false positives)

### Feature 02
- name: Unified domain CLI and deprecation wrappers
- description: Consolidated `src.cli` domain router plus deprecated `src.core.cli` and `src.services.cli` wrappers.
- status: partial
- entrypoints:
  - cli:python3 -m src.cli --help
  - cli:python3 -m src.core.cli --help
  - cli:python3 -m src.services.cli --help
- primary_files:
  - src/cli/__main__.py
  - src/core/cli/__main__.py
  - src/services/cli/__main__.py
- dependencies:
  - stdlib argparse/sys
  - expected downstream modules: `src.services.messaging_cli`, `src.services.contract_service`
- tests:
  - existing: no direct CLI tests found
  - missing: wrapper redirection tests and domain dispatch tests
- risks:
  - deprecated wrappers import `main` from `src.cli` package (not exported), yielding fallback errors
  - unified services messaging route imports non-existent module `src.services.messaging_cli`

### Feature 03
- name: Packaged agent-cellphone CLI (project script entrypoints)
- description: Pyproject-declared script set (`agent-cellphone*`) mapped to `src/agent_cellphone/cli.py`.
- status: broken
- entrypoints:
  - cli:agent-cellphone
  - cli:agent-cellphone-status
  - cli:python3 src/agent_cellphone/cli.py --help
- primary_files:
  - pyproject.toml
  - src/agent_cellphone/cli.py
- dependencies:
  - stdlib argparse
- tests:
  - existing: none found for this CLI file
  - missing: parser/command tests and script-install smoke tests
- risks:
  - syntax corruption in file body and trailing editor artifact tags
  - packaging exposes commands that cannot start

### Feature 04
- name: Unified messaging CLI (standalone script)
- description: Messaging script for direct agent delivery, onboarding, stats/history, with optional core-system integration.
- status: partial
- entrypoints:
  - cli:python3 messaging_cli_unified.py --help
  - cli:python3 messaging_cli_unified.py --agent Agent-1 --message "..."
- primary_files:
  - messaging_cli_unified.py
  - templates/session-closure-template.md
- dependencies:
  - pyautogui
  - pyperclip
  - optional core modules (`src.core.messaging_ssot`)
- tests:
  - existing: indirect messaging tests exist, but no direct tests for this script path
  - missing: CLI argument/exit-code matrix, delivery-mode tests, onboarding-path tests
- risks:
  - environment missing `pyautogui`/`pyperclip`, resulting in delivery failure
  - script advertises hybrid modes while implementation path is effectively pyautogui-only success criterion
  - history/stats are placeholder data in standalone mode

### Feature 05
- name: Messaging service layer (in-repo service API)
- description: Service-level messaging abstractions intended to back CLIs and coordination flows.
- status: stub
- entrypoints:
  - module:src.services.messaging_infrastructure.ConsolidatedMessagingService
  - module:src.services.unified_messaging_service.UnifiedMessagingService
- primary_files:
  - src/services/messaging_infrastructure.py
  - src/services/unified_messaging_service.py
  - src/services/messaging/cli_parser.py
- dependencies:
  - expected queue/models layers under `src.core` and `src.services.messaging.*`
- tests:
  - existing: tests/unit/services/test_messaging_infrastructure.py; tests/unit/services/test_unified_messaging_service.py
  - missing: contract-alignment tests to confirm implementations satisfy existing suite expectations
- risks:
  - current implementation files are minimal shims not matching tested public contracts
  - unresolved route to missing `src.services.messaging_cli`

### Feature 06
- name: System status and health CLI
- description: Swarm health/status CLI reporting filesystem-based health signals.
- status: exists
- entrypoints:
  - cli:python3 -m src.services.status_cli --health
  - cli:python3 -m src.services.status_cli --agents
  - cli:python3 -m src.services.status_cli --coordination
- primary_files:
  - src/services/status_cli.py
- dependencies:
  - stdlib argparse/json/pathlib/datetime
  - workspace paths: `agent_workspaces/`, `message_queue/`, `coordination_cache.json`
- tests:
  - existing: no direct tests found
  - missing: deterministic CLI contract tests for output schema and exit codes
- risks:
  - status is inferred from files, not live service process state
  - no machine-readable output flag for automation consumers

### Feature 07
- name: Safety foundation CLI
- description: CLI surface for kill switch, sandbox, blast-radius, audit trail, and snapshots.
- status: broken
- entrypoints:
  - cli:python3 -m src.core.safety.cli status
  - cli:python3 -m src.core.safety.cli kill-switch --trigger
- primary_files:
  - src/core/safety/cli.py
  - src/core/safety/*
- dependencies:
  - `src.core` package import path
  - config stack (`dotenv` transitively)
- tests:
  - existing: tests/standalone/test_safety_components.py
  - missing: explicit CLI argument/exit-code tests for each subcommand
- risks:
  - blocked by `dotenv` import via `src.core.__init__` before command execution

### Feature 08
- name: Workflow engine CLI
- description: CLI for creating/executing/listing workflow state machines.
- status: broken
- entrypoints:
  - cli:python3 -m src.workflows.cli create ...
  - cli:python3 -m src.workflows.cli execute ...
  - cli:python3 -m src.workflows.cli list
- primary_files:
  - src/workflows/cli.py
  - src/workflows/engine.py
  - src/workflows/models.py
- dependencies:
  - asyncio/json/pathlib
  - `src.core` serialization imports
- tests:
  - existing: engine/model tests exist; no direct CLI tests
  - missing: CLI acceptance tests for create/execute/status/pause/resume
- risks:
  - package import chain fails when `dotenv` unavailable
  - parser defines status/pause/resume but main dispatch handles only create/execute/list

### Feature 09
- name: Vision system CLI
- description: CLI for capture/OCR/analyze/monitor/info operations.
- status: broken
- entrypoints:
  - cli:python3 -m src.vision.cli capture ...
  - cli:python3 -m src.vision.cli ocr ...
  - cli:python3 -m src.vision.cli info
- primary_files:
  - src/vision/cli.py
  - src/vision/integration.py
  - src/vision/analysis.py
- dependencies:
  - pillow
  - numpy
  - pytesseract
  - opencv-python
  - `src.core` config path
- tests:
  - existing: no direct CLI tests found
  - missing: end-to-end CLI tests with fixture images and exit-code assertions
- risks:
  - import chain fails via `src.core` when `dotenv` missing
  - optional dependency behavior not fully contract-tested

### Feature 10
- name: Overnight autonomous orchestrator CLI
- description: CLI for starting/status/monitoring/recovery controls for overnight automation.
- status: broken
- entrypoints:
  - cli:python3 -m src.orchestrators.overnight.cli start ...
  - cli:python3 -m src.orchestrators.overnight.cli status
  - cli:python3 -m src.orchestrators.overnight.cli recovery
- primary_files:
  - src/orchestrators/overnight/cli.py
  - src/orchestrators/overnight/orchestrator.py
  - src/orchestrators/overnight/enhanced_agent_activity_detector.py
- dependencies:
  - asyncio
  - `src.core` imports
- tests:
  - existing: no direct CLI tests found
  - missing: CLI lifecycle tests and task-action tests
- risks:
  - `enhanced_agent_activity_detector.py` compile error blocks package load
  - eager imports in `src/orchestrators/overnight/__init__.py` amplify blast radius

### Feature 11
- name: Trader replay journal CLI
- description: Trading replay session create/start/step/pause/status command surface.
- status: broken
- entrypoints:
  - cli:python3 -m src.services.trader_replay.trader_replay_cli --help
  - cli:python3 -m src.services.trader_replay.trader_replay_cli create ...
- primary_files:
  - src/services/trader_replay/trader_replay_cli.py
  - src/services/trader_replay/trader_replay_orchestrator.py
- dependencies:
  - sqlite persistence layer
  - `src.core.base.base_service` import chain
- tests:
  - existing: tests/integration/trader_replay/test_cli_smoke.py and replay repository tests
  - missing: test coverage for dotenv/import-failure startup modes and list command behavior contract
- risks:
  - current runtime blocked by `dotenv` import chain
  - list command explicitly marked placeholder

### Feature 12
- name: TSLA morning report pipeline CLI
- description: Morning report build/publish, recommendation scoring, weekly summary.
- status: broken
- entrypoints:
  - cli:python3 -m src.trading_robot.tsla_report.cli.tsla_report_cli morning_report
  - cli:python3 -m src.trading_robot.tsla_report.cli.tsla_report_cli score_recommendations
  - cli:python3 -m src.trading_robot.tsla_report.cli.tsla_report_cli weekly_summary
- primary_files:
  - src/trading_robot/tsla_report/cli/tsla_report_cli.py
  - src/trading_robot/tsla_report/publisher/__init__.py
  - src/trading_robot/tsla_report/reporting.py
  - src/trading_robot/tsla_report/ledger/*
- dependencies:
  - provider API key env vars
  - discord publisher module expected at `publisher/discord.py`
- tests:
  - existing: no direct CLI tests found
  - missing: CLI startup tests, ledger-write tests, dry-run publish tests
- risks:
  - required module `src.trading_robot.tsla_report.publisher.discord` missing
  - publisher package currently contains only `__init__.py`

### Feature 13
- name: Open-source contribution CLI
- description: OSS project clone/list/issues/pr/portfolio/status operations.
- status: broken
- entrypoints:
  - cli:python3 -m src.opensource.oss_cli clone ...
  - cli:python3 -m src.opensource.oss_cli list
- primary_files:
  - src/opensource/oss_cli.py
  - src/opensource/project_manager.py
  - src/opensource/github_integration.py
- dependencies:
  - GitHub integration modules
  - `src.core` config constants
- tests:
  - existing: none specific to `oss_cli.py` found
  - missing: parser and command-path tests
- risks:
  - package import chain fails before CLI parser due `dotenv` dependency transitively

### Feature 14
- name: ChatGPT integration CLI
- description: Browser/session/conversation extraction CLI for ChatGPT workflows.
- status: broken
- entrypoints:
  - cli:python3 -m src.services.chatgpt.cli navigate
  - cli:python3 -m src.services.chatgpt.cli send --message "..."
  - cli:python3 -m src.services.chatgpt.cli extract
- primary_files:
  - src/services/chatgpt/cli.py
  - src/services/chatgpt/navigator.py
  - src/services/chatgpt/extractor.py
  - src/services/chatgpt/session.py
- dependencies:
  - playwright/browser automation stack
  - `src.core` base service chain
- tests:
  - existing: tests/unit/services/test_navigator.py, test_session.py, test_extractor_* files
  - missing: direct CLI acceptance tests
- risks:
  - import chain fails via `src.core`/dotenv before command dispatch
  - package `__init__` eager imports expand failure scope

### Feature 15
- name: Analytics readiness CLI tool
- description: Checks websites directory/config files/ID formats and prints readiness report.
- status: broken
- entrypoints:
  - cli:python3 -m src.tools.analytics_readiness_cli --full-report
- primary_files:
  - src/tools/analytics_readiness_cli.py
- dependencies:
  - filesystem under `websites/`
- tests:
  - existing: none found
  - missing: parser and report-output tests
- risks:
  - syntax error (`print(".1f"`) prevents module execution
  - package import path also blocked by tools package eager import requiring `dotenv`

### Feature 16
- name: System discovery agent CLI tool
- description: Search/recommend/learn/training assistant for internal systems catalog.
- status: broken
- entrypoints:
  - cli:python3 -m src.tools.system_discovery_agent --search "..."
- primary_files:
  - src/tools/system_discovery_agent.py
- dependencies:
  - stdlib only (intended)
- tests:
  - existing: none found
  - missing: parser, ranking, recommendation contract tests
- risks:
  - trailing editor artifact tags produce syntax error
  - package import currently blocked by `src.tools.__init__` importing dotenv-dependent module

### Feature 17
- name: Risk analytics services and API modules
- description: Risk metric calculators and WordPress-style endpoint handlers.
- status: exists
- entrypoints:
  - module:python3 -m src.services.risk_analytics.risk_api_endpoints
  - module:python3 -m src.services.risk_analytics.risk_calculator_service
- primary_files:
  - src/services/risk_analytics/risk_api_endpoints.py
  - src/services/risk_analytics/risk_calculator_service.py
- dependencies:
  - numpy
  - optional pandas
- tests:
  - existing: tests/unit/services/test_risk_api_endpoints.py, tests/unit/services/test_risk_calculator_service.py
  - missing: runtime integration tests against real WP request/response layer
- risks:
  - `_get_trading_data` currently returns mock data, not repository-backed market/performance data

### Feature 18
- name: Unified persistence infrastructure
- description: Unified repository facade over agent/task persistence and DB stats/backup helpers.
- status: partial
- entrypoints:
  - module:python3 -m src.infrastructure.unified_persistence
- primary_files:
  - src/infrastructure/unified_persistence.py
  - src/infrastructure/persistence/*
  - src/infrastructure/__init__.py
- dependencies:
  - sqlite
  - persistence model/repository classes
- tests:
  - existing: tests/unit/infrastructure/test_unified_persistence.py and repository tests
  - missing: executable module-entry smoke in clean env and backup/restore integration tests
- risks:
  - module execution is blocked by `src.infrastructure.__init__` importing browser stack (which imports dotenv-dependent core)

### Feature 19
- name: Unified browser infrastructure service
- description: Browser/session/cookie facade intended for Thea/Chat workflows.
- status: partial
- entrypoints:
  - module:python3 -m src.infrastructure.unified_browser_service
- primary_files:
  - src/infrastructure/unified_browser_service.py
  - src/infrastructure/browser/browser_models.py
  - src/infrastructure/browser/unified_cookie_manager.py
- dependencies:
  - browser driver stack (expected)
  - Thea configs
- tests:
  - existing: tests/unit/infrastructure/test_unified_browser_service.py + browser unit tests
  - missing: non-stub browser-adapter integration tests
- risks:
  - core adapter/ops/session classes in file are stubs returning false/empty values
  - module execution blocked by package-level dotenv dependency chain

### Feature 20
- name: Swarm brain knowledge base
- description: Shared JSON+markdown knowledge storage and query layer.
- status: exists
- entrypoints:
  - module:python3 -m src.swarm_brain.knowledge_base
- primary_files:
  - src/swarm_brain/knowledge_base.py
  - src/swarm_brain/agent_notes.py
  - src/swarm_brain/swarm_memory.py
- dependencies:
  - stdlib json/pathlib/datetime
  - filesystem under `swarm_brain/`
- tests:
  - existing: tests/unit/swarm_brain/test_knowledge_base.py, test_agent_notes.py, test_swarm_memory.py
  - missing: concurrency/locking tests for parallel writes
- risks:
  - no file-locking around writes; race conditions possible in multi-agent parallel updates

### Feature 21
- name: Project scanner integration
- description: Scanner orchestration with cache and Thea-guidance generation.
- status: partial
- entrypoints:
  - module:python3 -m src.core.project_scanner_integration scan
- primary_files:
  - src/core/project_scanner_integration.py
  - src/services/repository_monitor.py
  - src/core/gasline_integrations.py
- dependencies:
  - optional external scanner in `temp_repos/Auto_Blogger/project_scanner.py`
  - fallback `tools/simple_project_scanner.py`
  - Thea service integration
- tests:
  - existing: no dedicated tests found
  - missing: scanner-cache contract tests and Thea prompt/guidance tests
- risks:
  - duplicate method definitions in same class (`_get_thea_guidance`, `_build_thea_prompt` each defined twice)
  - runtime blocked in package mode by core dotenv dependency

---

## Cross-feature dependency health (observed)

- Missing imports in current environment:
  - `dotenv`, `pyautogui`, `pyperclip`, `pytest`
- Packaging drift:
  - `pyproject.toml [project].dependencies = []` while `data/requirements.txt` declares runtime packages
- Compile health:
  - 21 syntax/indentation/conflict-marker failures under `src/`
- Docstring coverage snapshot (`src`):
  - parseable files with module docstrings: 1055
  - parseable files missing module docstrings: 147
  - unparsable files: 21
