# dream.os - Multi-Stage Docker Build
# ================================================

# Base stage with Python and system dependencies
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    htop \
    procps \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    AGENT_CELLPHONE_ENV=docker

# Create application user
RUN useradd --create-home --shell /bin/bash agent
USER agent

# Application stage
FROM base as application

# Copy requirements first for better caching
COPY --chown=agent:agent requirements*.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt && \
    pip install --no-cache-dir --user -e .

# Copy application code
COPY --chown=agent:agent . /app/

# Create necessary directories
RUN mkdir -p /app/agent_workspaces /app/logs /app/runtime /app/pids /app/data

# Set working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "from src.core.health_check import check_system_health; check_system_health()" || exit 1

# Default command
CMD ["python", "main.py", "--background"]