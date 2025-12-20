# Trading Robot Dependency Validation Documentation

**Created**: 2025-12-20  
**Author**: Agent-3 (Infrastructure & DevOps Specialist)

## Overview

This document describes the dependency validation process for the Trading Robot project, including requirements.txt validation, virtual environment setup, and dependency conflict resolution.

## Requirements

- Python 3.11+ (tested with Python 3.11.9)
- pip (latest version recommended)

## Dependencies

The trading robot requires 28 dependencies listed in `requirements.txt`:

### Core Trading Dependencies
- `alpaca-py>=2.0.0` - Alpaca trading API client
- `robin-stocks>=1.0.0` - Robinhood integration (optional, unofficial)

### Data Processing
- `pandas>=1.5.0` - Data manipulation and analysis
- `numpy>=1.21.0` - Numerical computing
- `matplotlib>=3.5.0` - Plotting and visualization
- `seaborn>=0.11.0` - Statistical visualization
- `plotly>=5.0.0` - Interactive plots

### Web Framework
- `fastapi>=0.100.0` - Modern web framework
- `uvicorn>=0.23.0` - ASGI server
- `python-multipart>=0.0.6` - Multipart form data support
- `jinja2>=3.1.0` - Template engine

### Database
- `sqlalchemy>=2.0.0` - SQL toolkit and ORM
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter

### Task Queue
- `redis>=4.5.0` - Redis client
- `celery>=5.3.0` - Distributed task queue

### Testing
- `pytest>=7.0.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async test support

### Utilities
- `python-dotenv>=1.0.0` - Environment variable management
- `aiohttp>=3.8.0` - Async HTTP client
- `websockets>=11.0.0` - WebSocket support
- `cryptography>=41.0.0` - Cryptographic library
- `pytz>=2023.3` - Timezone support
- `schedule>=1.2.0` - Job scheduling
- `loguru>=0.7.0` - Logging
- `pydantic>=2.0.0` - Data validation
- `pydantic-settings>=2.0.0` - Settings management
- `httpx>=0.24.0` - HTTP client
- `asyncio-mqtt>=0.13.0` - MQTT support

## Validation Process

### Method 1: Quick Validation (Recommended)

Check if requirements.txt is parseable and all packages are valid:

```bash
cd trading_robot
python scripts/validate_dependencies.py
```

This script:
1. Parses `requirements.txt`
2. Validates package names and version specifiers
3. Creates virtual environment setup scripts

### Method 2: Manual Validation

Check requirements.txt syntax:

```bash
pip install --dry-run -r requirements.txt
```

### Method 3: Virtual Environment Test

Create a clean virtual environment and install all dependencies:

```bash
# Linux/Mac
./setup_venv.sh

# Windows
setup_venv.bat
```

Or manually:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

## Virtual Environment Setup

### Automated Setup

Use the provided setup scripts:

**Linux/Mac:**
```bash
./setup_venv.sh
```

**Windows:**
```cmd
setup_venv.bat
```

### Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Dependency Conflicts

### Known Issues

1. **robin-stocks**: Unofficial library, use at own risk. Comment in requirements.txt must be on separate line.

2. **Version conflicts**: If you encounter version conflicts:
   ```bash
   pip install --upgrade pip
   pip install --upgrade -r requirements.txt
   ```

### Resolving Conflicts

1. **Check conflict details:**
   ```bash
   pip check
   ```

2. **Identify conflicting packages:**
   ```bash
   pip list --outdated
   ```

3. **Update specific packages:**
   ```bash
   pip install --upgrade package_name
   ```

## Testing Installation

After installation, verify key imports:

```python
# Test core dependencies
import alpaca
import pandas as pd
import numpy as np
import fastapi
import sqlalchemy
import loguru

print("✅ All core dependencies imported successfully")
```

## Clean Installation

To start with a clean environment:

```bash
# Remove existing virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Create new virtual environment
python -m venv venv

# Activate and install
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

## Dependency Lock File (Optional)

For production deployments, consider creating a lock file:

```bash
pip freeze > requirements-lock.txt
```

This ensures exact versions are installed in production.

## Troubleshooting

### Issue: "Invalid requirement" error

**Solution**: Check for comments on the same line as package names. Comments must be on separate lines in requirements.txt.

### Issue: Package installation timeout

**Solution**: Increase pip timeout or check network connection:
```bash
pip install --default-timeout=100 -r requirements.txt
```

### Issue: PostgreSQL adapter fails on Windows

**Solution**: Use pre-built binary:
```bash
pip install psycopg2-binary
```

### Issue: Redis connection errors

**Solution**: Redis is optional for basic functionality. Ensure Redis server is running if using Celery features.

## Next Steps

1. ✅ **Validate dependencies** - Use validation script
2. ✅ **Create virtual environment** - Use setup scripts
3. ✅ **Install dependencies** - `pip install -r requirements.txt`
4. ⏭️ **Configure environment** - Set up `.env` file (see `ENV_SETUP_DOCUMENTATION.md`)
5. ⏭️ **Initialize database** - Run `python scripts/init_database.py`
6. ⏭️ **Test installation** - Run basic import tests

## See Also

- `ENV_SETUP_DOCUMENTATION.md`: Environment variable configuration
- `DATABASE_SCHEMA.md`: Database setup and schema
- `scripts/validate_dependencies.py`: Dependency validation script
- `scripts/init_database.py`: Database initialization script
