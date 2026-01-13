# Contributing to Agent Cellphone V2

Welcome to the Agent Cellphone V2 project! This document provides guidelines for contributors who want to help improve and extend this multi-agent swarm intelligence system.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- Familiarity with Discord bot development
- Understanding of multi-agent systems

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/agent-cellphone-v2.git
   cd agent-cellphone-v2
   ```

2. **Set up the environment:**
   ```bash
   # Copy environment template
   cp env.example .env

   # Configure Discord credentials (required)
   # Edit .env file with your bot token and server ID
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   DISCORD_GUILD_ID=your_discord_server_id_here
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run tests:**
   ```bash
   python -m pytest
   ```

## 🏗️ Project Structure

```
agent-cellphone-v2/
├── src/
│   ├── core/                 # Core system components
│   ├── services/            # Service layer implementations
│   ├── discord_commander/   # Discord bot functionality
│   └── agents/              # Agent implementations
├── examples/                # Example usage scripts
├── docs/                   # Documentation
├── tests/                  # Test suites
├── tools/                  # Development tools
└── scripts/                # Utility scripts
```

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all public methods
- Write comprehensive docstrings
- Maximum line length: 100 characters

### V2 Compliance Requirements
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Modular Architecture**: Each module <300 lines, <5 classes, <10 functions
- **SSOT (Single Source of Truth)**: No code duplication, centralized configuration
- **Comprehensive Testing**: Unit tests, integration tests, smoke tests

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🎯 Contribution Types

### 🐛 Bug Fixes
- Create a detailed bug report with reproduction steps
- Write a failing test case first
- Implement the fix
- Ensure all tests pass

### ✨ New Features
- Discuss feature ideas in GitHub Issues first
- Follow the feature development workflow:
  1. Create feature branch: `git checkout -b feature/your-feature-name`
  2. Implement feature with tests
  3. Update documentation
  4. Submit pull request

### 📚 Documentation
- Keep README.md updated
- Add docstrings to new public methods
- Update API documentation
- Create usage examples

### 🧪 Testing
- Write unit tests for new functionality
- Update integration tests as needed
- Maintain >80% test coverage
- Run full test suite before submitting PR

## 🔧 Development Workflow

### 1. Choose a Task
- Check GitHub Issues for open tasks
- Look for "good first issue" or "help wanted" labels
- Coordinate with other agents via the messaging system

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Development Process
```bash
# Make changes
# Write tests
python -m pytest tests/

# Run linting
python -m flake8 src/
python -m black src/

# Update documentation
# Commit changes
```

### 4. Testing Your Changes
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# End-to-end tests
python -m pytest tests/e2e/
```

### 5. Submit Pull Request
- Ensure all tests pass
- Update CHANGELOG.md if needed
- Request review from relevant agents
- Address review feedback

## 🤖 Agent Communication

### Messaging System
Use the built-in messaging system for agent coordination:

```bash
# Send message to specific agent
python -m src.services.messaging_cli --agent Agent-X --message "Coordination message"

# Send to all agents
python -m src.services.messaging_cli --broadcast --message "System announcement"
```

### Task Assignment Protocol
```
TASK ASSIGNMENT: [Role Title]
Assigned tasks: [Task 1], [Task 2], [Task 3]
Timeline: Complete by [Date]
Priority: [P0/P1/P2] - [Priority description]
Capabilities required: [Skill 1], [Skill 2]
Coordinate with: [Agent names] for [specific tasks]
```

## 🧪 Testing Strategy

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Focus on business logic

### Integration Tests
- Test component interactions
- Verify service layer functionality
- Test database operations

### End-to-End Tests
- Test complete user workflows
- Verify system integration
- Test performance requirements

### Smoke Tests
- Basic functionality verification
- Run after deployments
- Quick regression detection

## 📊 Code Quality Metrics

### V2 Compliance Checklist
- [ ] Module size <300 lines
- [ ] Class count <5 per module
- [ ] Function count <10 per module
- [ ] SOLID principles followed
- [ ] Comprehensive docstrings
- [ ] Type hints on public methods
- [ ] Unit test coverage >80%
- [ ] Integration tests present

### Performance Targets
- Response time <100ms for API calls
- Memory usage <100MB per agent
- CPU usage <20% during normal operation
- Test execution <60 seconds

## 🚀 Deployment

### Development Environment
```bash
# Start all services
python tools/start_services.py

# Check system health
python -m src.services.messaging_cli --health-check
```

### Production Deployment
```bash
# Build production image
docker build -t agent-cellphone-v2 .

# Deploy with docker-compose
docker-compose up -d
```

## 📞 Support

### Getting Help
- Check existing GitHub Issues
- Review documentation in `docs/`
- Run examples in `examples/`
- Contact Agent-4 (Captain) for coordination

### Reporting Issues
- Use GitHub Issues for bugs and features
- Include reproduction steps
- Attach relevant logs
- Tag appropriate agents

## 🎖️ Recognition

Contributors are recognized through:
- GitHub contributor statistics
- Agent performance metrics
- Swarm intelligence acknowledgments
- Documentation credits

Thank you for contributing to Agent Cellphone V2! Your work helps advance multi-agent swarm intelligence. 🐝⚡️🔥

---

*This document follows V2 compliance standards and is maintained by Agent-7 (Documentation & CLI Enhancement Lead)*