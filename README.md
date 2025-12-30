# Agent Cellphone V2 - AutoDream OS

**A multi-agent autonomous system for software development, automation, and infrastructure management.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![V2 Compliance](https://img.shields.io/badge/V2-Compliant-green.svg)](STANDARDS.md)

---

## 📋 Table of Contents

- [Overview](#overview)
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

Agent Cellphone V2 is an autonomous multi-agent system designed for:
- **Software Development**: Automated code refactoring, testing, and quality assurance
- **Infrastructure Management**: Browser automation, deployment, and monitoring
- **Communication**: Discord bot integration, messaging, and coordination
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

### Integrations

- **Discord**: Bot commands, messaging, webhooks
- **GitHub**: Repository management, PR automation
- **WordPress**: Blog management and deployment
- **Trading Systems**: Automated trading robot integration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git
- (Optional) Node.js for web components

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Agent_Cellphone_V2_Repository

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
cp env.example .env
# Edit .env with your configuration

# Verify installation
python -m pytest tests/ --version
```

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
- **[AGENTS.md](AGENTS.md)**: Agent system documentation
- **[docs/](docs/)**: Additional documentation and guides
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


