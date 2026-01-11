# Agent Cellphone V2 - Production Docker Image
# ================================================

# Use Python 3.11 slim image for smaller footprint
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r agentcellphone && useradd -r -g agentcellphone agentcellphone

# Set work directory
WORKDIR /app

# Copy package files first for better caching
COPY pyproject.toml setup.py requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Install the package
RUN pip install -e .

# Create necessary directories
RUN mkdir -p data logs agent_workspaces screenshots && \
    chown -R agentcellphone:agentcellphone /app

# Switch to non-root user
USER agentcellphone

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Default command
CMD ["python", "main.py"]