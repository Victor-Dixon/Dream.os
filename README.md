# Agent Cellphone V2

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional multi-agent coordination system for automated task management, real-time collaboration, and intelligent workflow orchestration.

## Features

- **🤖 Multi-Agent Coordination**: Swarm intelligence for collaborative task execution
- **⚡ Real-Time Collaboration**: Operational Transformation (OT) and CRDT for conflict-free editing
- **🎯 AI-Powered UX**: Context-aware user experience with predictive personalization
- **📊 Intelligent Analytics**: AI-driven insights and automated recommendations
- **🚀 FastAPI Integration**: High-performance REST API with automatic documentation
- **💬 Discord Integration**: Seamless agent communication and coordination
- **🐳 Docker Support**: Easy deployment and portability
- **🔒 Professional Security**: Environment-based configuration and secrets management

## Quick Start

### Prerequisites

- Python 3.11+
- pip (latest version recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dadudekc/agent-cellphone-v2.git
   cd agent-cellphone-v2
   ```

2. **Install the package:**
   ```bash
   # For development
   pip install -e .[dev,test]

   # For production
   pip install .
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Start the system:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8001` and the documentation at `http://localhost:8001/docs`.

## Docker Deployment

For easy deployment and portability:

```bash
# Build the image
docker build -t agent-cellphone-v2 .

# Run with environment file
docker run -p 8001:8001 --env-file .env agent-cellphone-v2
```

Or use Docker Compose:

```bash
docker-compose up -d
```

## Configuration

The system uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```bash
# Application Settings
DEBUG=false
API_HOST=0.0.0.0
API_PORT=8001

# Discord Integration (optional)
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id

# Database
DATABASE_URL=sqlite:///agent_cellphone.db

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Usage

### Command Line Interface

```bash
# Start the system
python main.py

# Check status
python main.py --status

# Stop services
python main.py --stop

# API only mode
python main.py --api-only
```

### Python API

```python
from agent_cellphone_v2 import AgentCoordinator

# Initialize coordinator
coordinator = AgentCoordinator()

# Start the system
await coordinator.start()

# Send a message to an agent
result = await coordinator.send_message("agent-1", "Hello from coordinator!")

# Get system status
status = await coordinator.get_status()

# Stop the system
await coordinator.stop()
```

### REST API

The system provides a comprehensive REST API:

```bash
# Health check
curl http://localhost:8001/health

# System status
curl http://localhost:8001/status

# API documentation
open http://localhost:8001/docs
```

## Architecture

### Core Components

- **AgentCoordinator**: Main orchestration engine
- **MessagingService**: Inter-agent communication
- **APIService**: REST API endpoints
- **Configuration**: Environment-based settings management

### Directory Structure

```
agent-cellphone-v2/
├── src/
│   └── agent_cellphone_v2/
│       ├── __init__.py
│       ├── __version__.py
│       ├── core.py                 # Main coordinator
│       ├── config.py              # Configuration management
│       └── services/
│           ├── __init__.py
│           ├── messaging.py       # Messaging service
│           └── api.py            # API service
├── tests/                        # Test suite
├── docs/                         # Documentation
├── docker/                       # Docker files
├── .env.example                  # Environment template
├── setup.py                      # Package installation
├── pyproject.toml               # Build configuration
├── main.py                      # CLI entry point
└── README.md                    # This file
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e .[dev,test]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
black src/
flake8 src/
mypy src/
```

### Code Quality

This project follows strict code quality standards:

- **Formatting**: Black
- **Linting**: Flake8
- **Type Checking**: MyPy
- **Testing**: Pytest with coverage reporting
- **Pre-commit**: Automated quality checks

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## API Documentation

When running, visit `http://localhost:8001/docs` for interactive API documentation.

## Security

- All sensitive configuration uses environment variables
- No hardcoded secrets or credentials
- Configurable allowed hosts for production deployment
- Environment-based configuration for different deployment stages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/dadudekc/agent-cellphone-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/dadudekc/agent-cellphone-v2/discussions)
- **Documentation**: [Read the Docs](https://agent-cellphone-v2.readthedocs.io/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

**Built with ❤️ for the swarm intelligence revolution**