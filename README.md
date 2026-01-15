
**A multi-agent autonomous system for software development, automation, and infrastructure management.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![V2 Compliance](https://img.shields.io/badge/V2-Compliant-green.svg)](STANDARDS.md)

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Reliability](#system-reliability)
- [Architecture](#architecture)
- [Key Components](#key-components)
- [Quick Start](#quick-start)
- [Development Standards](#development-standards)
- [Agent System](#agent-system)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Documentation](#documentation)

---

## 🎯 Overview

dream.os is an autonomous multi-agent system designed for:
- **Software Development**: Automated code refactoring, testing, and quality assurance
- **Infrastructure Management**: Browser automation, deployment, and monitoring
- **Communication**: Discord bot integration, messaging, and coordination

---

## 🔧 System Reliability

dream.os maintains high system reliability through systematic runtime error resolution and infrastructure validation:

### Runtime Error Resolution Protocol
- **Systematic Diagnosis**: Automated identification of import failures, syntax errors, and missing components
- **Prioritized Fixing**: Critical infrastructure components addressed first (Discord, trading, messaging)
- **Integration Testing**: Automated validation of fixes across the entire system
- **Continuous Monitoring**: Runtime error baseline established and tracked

### Reliability Metrics
- **Import Success Rate**: 100% of tested modules import successfully post-resolution
- **Infrastructure Uptime**: Major systems (Discord, trading, messaging) fully operational
- **Error Resolution Rate**: 59% improvement in system reliability (19/32 runtime errors resolved)

### Quality Assurance
- **Automated Testing**: Integration testing protocols for ongoing validation
- **Documentation Standards**: V2 compliance with comprehensive error handling
- **Coordination Protocols**: Swarm coordination with environmental dependency management

---
- **Data Processing**: Trading systems, analytics, and business intelligence

The system follows **V2 Compliance Standards** (files ~400 lines guideline, clean code principles prioritized) and implements **SOLID principles** throughout.

---

## 🏗️ Architecture

### Core Principles

- **Modular Design**: Single responsibility per module (~400 lines guideline, clean code principles)
- **SOLID Compliance**: Dependency injection, clear boundaries
- **Repository Pattern**: Data access abstraction
- **Service Layer**: Business logic isolation
- **Type Safety**: Comprehensive type hints

### Architecture Layers

```
┌─────────────────────────────────────┐
│   Presentation Layer                │
│   (Discord, Web, GUI)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Service Layer                      │
│   (Business Logic)                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Repository Layer                   │
│   (Data Access)                      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Infrastructure Layer              │
│   (Browser, Logging, Persistence)    │
└─────────────────────────────────────┘
```

---

## 🔧 Key Components

### Core Systems

- **`src/core/`**: Core utilities, messaging, GitHub integration, activity detection
- **`src/services/`**: Business logic services (messaging, coordination, monitoring)
- **`src/infrastructure/`**: Browser automation, logging, persistence
- **`src/discord_commander/`**: Discord bot integration and commands
- **`src/orchestrators/`**: Overnight automation and task orchestration

### Infrastructure

- **Browser Automation**: Thea browser service for ChatGPT automation
- **Message Queue**: Persistent message queuing with retry mechanisms
- **Activity Detection**: Multi-source agent activity monitoring
- **GitHub Integration**: Synthetic GitHub wrapper with local-first strategy

### Packaging & Deployment

- **🐳 Docker**: Containerized deployment with docker-compose
- **📦 Python Package**: PyPI distribution ready
- **⚙️ Configuration**: Environment-based config management
- **🔄 Auto-Updates**: Built-in update and health monitoring
- **📊 Monitoring**: Comprehensive system health checks
- **💾 Backup/Restore**: Automated data protection

### Integrations

- **Discord**: Bot commands, messaging, webhooks
- **GitHub**: Repository management, PR automation
- **WordPress**: Blog management and deployment
- **Trading Systems**: Automated trading robot integration

### TradingRobotPlug TSLA Morning Report

The TSLA morning report pipeline produces a single-source-of-truth snapshot, renders a Discord-ready report, archives artifacts, and records recommendations for accuracy tracking.

**Location**
- `src/trading_robot/tsla_report/` (providers, features, engine, reports, publisher, ledger, cli)

**Environment**
- `ALPHA_VANTAGE_API_KEY` (required for market data)
- `TSLA_MARKET_PROVIDER` (optional, default: `alpha_vantage`)
- `DISCORD_WEBHOOK_URL` (required for posting; optional for `--dry-run`)

**CLI Usage**
```bash
# Build snapshot, render report, archive artifacts, save to ledger, publish to Discord
python -m src.trading_robot.tsla_report.cli.tsla_report_cli morning_report

# Dry run (prints Discord payload instead of posting)
python -m src.trading_robot.tsla_report.cli.tsla_report_cli morning_report --dry-run

# Score recommendations for a date (YYYY-MM-DD), defaults to today
python -m src.trading_robot.tsla_report.cli.tsla_report_cli score_recommendations --date 2026-01-05

# Weekly summary from the SQLite ledger
python -m src.trading_robot.tsla_report.cli.tsla_report_cli weekly_summary
```

**Artifacts**
- `data/devlogs/YYYY-MM-DD/analysis_snapshot.json`
- `data/devlogs/YYYY-MM-DD/report.md`
- `data/devlogs/YYYY-MM-DD/discord_payload.json`

---

## 🚀 Quick Start
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console

**Get dream.os running in under 5 minutes!**


**The easiest way to get started:**

```bash
# Clone and complete setup in one command!
git clone <repository-url>
cd Agent_Cellphone_V2_Repository
python setup.py
```

That's it! The interactive setup script will:
- ✅ Validate your system
- ✅ Guide you through configuration
- ✅ Install dependencies
- ✅ Start all services
- ✅ Verify everything works

### Prerequisites

- Python 3.11+ **OR** Docker Desktop
- Git (for cloning)
- 4GB RAM, 10GB disk space

### Installation Options

#### 🐳 Docker (Recommended - 2 minutes)
```bash
git clone <repository-url>
cd Agent_Cellphone_V2_Repository
python setup.py --docker
```

#### 🐍 Native Python (5 minutes)
```bash
git clone <repository-url>
cd Agent_Cellphone_V2_Repository
python setup.py --native
```

#### 🪟 Windows
```batch
git clone <repository-url>
cd Agent_Cellphone_V2_Repository
python setup.py
```

### First Validation

Before setup, validate your environment:

```bash
python scripts/post_clone_check.py
```

This checks:
- ✅ Python version compatibility
- ✅ Operating system support
- ✅ Required files present
- ✅ Disk space availability
- ✅ Docker availability (optional)

### Access Points

After successful setup:

- 🌐 **Web Dashboard**: http://localhost:5000
- 📚 **API Documentation**: http://localhost:8001/docs
- 🤖 **Discord Bot**: Ready for commands
- 📊 **Monitoring**: http://localhost:3000 (admin/admin123)

### Management Commands

```bash
# Check system status
python main.py --status

# Start/stop services
python main.py --background  # Start all
python main.py --stop        # Stop all

# Health monitoring
python scripts/health_check.py --check

# View logs
tail -f logs/app.log
```

📖 **[Platform Setup Guide](PLATFORM_SETUP.md)** | **[Quick Start Details](QUICKSTART.md)**

### Basic Usage

```bash
# Start Discord bot
python -m src.discord_commander.unified_discord_bot

# Run message queue processor
python tools/start_message_queue_processor.py

# Check system status
python tools/check_queue_status.py
```

---

## 📏 Development Standards

### V2 Compliance

- **Files**: ~400 lines guideline (clean code principles take precedence over line counts)
- **Classes**: ≤200 lines
- **Functions**: ≤30 lines
- **Enforcement**: Pre-commit hooks and CI/CD validation

See [STANDARDS.md](STANDARDS.md) for complete standards.

### Code Quality

- **Linting**: `ruff`, `flake8`, `pylint`
- **Formatting**: `black`, `isort`
- **Type Checking**: `mypy`
- **Testing**: `pytest` with ≥85% coverage

### Git Workflow

- **Commits**: Conventional format (`feat:`, `fix:`, `docs:`, etc.)
- **Branches**: `main` (production), `develop` (integration)
- **PRs**: Required code review and CI checks

---

## 🤖 Agent System

The system uses **8 specialized agents** for parallel execution:

| Agent | Role | Domain |
|-------|------|--------|
| **Agent-1** | Integration & Core Systems | Integration layer, GitHub, messaging |
| **Agent-2** | Architecture & Design | Architecture reviews, design patterns |
| **Agent-3** | Infrastructure & DevOps | Browser automation, infrastructure refactoring |
| **Agent-4** | Captain (Strategic Oversight) | Task assignment, system monitoring |
| **Agent-5** | Business Intelligence | Analytics, reporting, metrics |
| **Agent-6** | Coordination & Communication | Monitoring, coordination protocols |
| **Agent-7** | Web Development | Web components, frontend |
| **Agent-8** | SSOT & System Integration | Single source of truth, QA validation |

### Agent Coordination

- **Status Tracking**: `agent_workspaces/{Agent-X}/status.json`
- **Messaging**: Unified messaging system with inbox/outbox
- **Coordination**: Bilateral and swarm-wide protocols
- **Validation**: Agent-8 QA validation workflow

See [AGENTS.md](AGENTS.md) for detailed agent documentation.

---

## 📁 Project Structure

```
Agent_Cellphone_V2_Repository/
├── src/                    # Source code
│   ├── core/              # Core utilities and systems
│   ├── services/          # Business logic services
│   ├── infrastructure/    # Infrastructure components
│   ├── discord_commander/ # Discord bot integration
│   ├── orchestrators/     # Task orchestration
│   └── web/              # Web components
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── tools/                # Utility scripts and tools
├── scripts/              # Organized scripts by purpose
│   ├── health/           # Health check scripts
│   ├── deployment/       # Deployment scripts
│   ├── debug/            # Debug utilities
│   └── tasks/            # Task management scripts
├── docs/                 # Documentation (organized by domain)
│   ├── guides/           # How-to guides and tutorials
│   ├── standards/        # Code standards and conventions
│   ├── protocols/        # Operational protocols
│   ├── architecture/     # System architecture docs
│   ├── planning/         # Planning documents (by year)
│   ├── archive/          # Historical documentation
│   │   ├── audits/       # Historical audit reports
│   │   ├── investigations/ # Investigation reports
│   │   ├── reports/      # Historical status reports
│   │   └── task_logs/    # Historical task logs
│   └── ...               # Additional documentation
├── data/                 # Data files (organized by type)
│   ├── ssot/             # SSOT-related data
│   ├── cache/            # Cache files
│   └── feeds/            # Feed data
├── reports/              # Current reports
│   ├── ssot/             # SSOT-related reports
│   └── data/             # Report data files
├── config/               # Configuration files
├── agent_workspaces/     # Agent-specific workspaces
├── archive/              # Archived files
│   └── temp/             # Temporary archived files
├── README.md             # This file (project entry point)
├── CHANGELOG.md          # Project changelog
├── MASTER_TASK_LOG.md    # Active task log
└── requirements.txt      # Python dependencies
```

**Note:** This structure was reorganized in December 2025 for improved maintainability and discoverability. Historical files are archived in `docs/archive/` and `archive/` directories.

---

## 📚 Documentation

- **[STANDARDS.md](STANDARDS.md)**: Code quality and architecture standards
- **[DEPRECATION_NOTICES.md](docs/standards/DEPRECATION_NOTICES.md)**: Deprecation notices and migration guides
- **[AGENTS.md](AGENTS.md)**: Agent system documentation
- **[docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)**: Complete documentation navigation hub
- **[docs/guides/](docs/guides/)**: How-to guides and tutorials ([QUICK_START_GUIDE.md](docs/guides/QUICK_START_GUIDE.md), [DELEGATION_BOARD.md](docs/guides/DELEGATION_BOARD.md))
- **[docs/standards/](docs/standards/)**: Code standards and conventions
- **[docs/protocols/](docs/protocols/)**: Operational protocols and workflows
- **[docs/architecture/](docs/architecture/)**: System architecture documentation
- **[docs/archive/](docs/archive/)**: Historical documentation (archived by year/type)
- **Agent Workspaces**: `agent_workspaces/{Agent-X}/` for agent-specific docs

---

## 🤝 Contributing

### Development Workflow

1. **Claim Task**: Check available tasks in agent workspaces
2. **Sync**: Update from main branch
3. **Slice**: Break task into executable slices
4. **Execute**: Implement with V2 compliance
5. **Validate**: Run tests and linting
6. **Commit**: Use conventional commit format
7. **Report**: Update status.json and notify team

### Code Review Requirements

- All changes require code review
- PRs must pass CI checks (lint, test, build)
- Large features split into smaller PRs
- Documentation updated for new features

---

## 🔍 Key Features

### Message Queue System
- Persistent JSON-based queue
- Retry mechanisms and error handling
- Lock file management
- Diagnostic and fix tools

### Browser Automation
- Thea browser service for ChatGPT
- Auto-healing element discovery
- Cookie management
- Profile support

### GitHub Integration
- Synthetic GitHub wrapper
- Local-first strategy
- Sandbox mode support
- Deferred push queue

### Activity Detection
- Multi-source monitoring
- Confidence scoring
- Noise filtering
- Validation workflows

---

## 🛠️ Tools

### Diagnostic Tools
- `tools/diagnose_message_queue.py`: Queue diagnostics
- `tools/fix_message_queue.py`: Queue repair
- `tools/check_queue_status.py`: Quick status check

### Development Tools
- `tools/v2_compliance_checker.py`: V2 compliance validation
- `tools/integration_test_coordinator.py`: Test coordination
- `tools/audit_dadudekc_blog_posts.py`: Blog auditing

---

## 📊 Current Status

### V2 Refactoring Progress

- **Batch 1**: Browser service refactoring (4/5 modules complete)
- **Batch 2**: Activity detector refactoring (1/4 modules complete)
- **Total Progress**: ~15% of infrastructure violations refactored

### System Health

- **Message Queue**: Operational with diagnostic tools
- **Browser Service**: Refactoring in progress
- **Agent Coordination**: Active and monitored
- **Test Coverage**: ≥85% maintained

---

## 📝 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

Built with:
- Python 3.11+
- Discord.py
- Selenium/Undetected ChromeDriver
- Pytest
- And many more open-source tools

---

**🐝 WE. ARE. SWARM. ⚡**

*For questions or issues, check agent workspaces or contact Agent-4 (Captain).*

