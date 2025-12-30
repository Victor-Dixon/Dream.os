# FastAPI Process Management Configuration

**Generated:** 2025-12-30  
**Deployment Coordinator:** Agent-3  
**Status:** ✅ Ready

---

## Overview

Process management configurations for FastAPI deployment. Choose the appropriate method based on your environment.

---

## Option 1: systemd (Linux - Recommended)

### Installation

1. **Copy service file:**
   ```bash
   sudo cp docs/deployment/fastapi.systemd.service /etc/systemd/system/fastapi.service
   ```

2. **Edit service file:**
   ```bash
   sudo nano /etc/systemd/system/fastapi.service
   ```
   
   Update the following paths:
   - `WorkingDirectory`: Path to Agent_Cellphone_V2_Repository
   - `ExecStart`: Path to venv/bin/uvicorn and correct module path
   - `EnvironmentFile`: Path to .env file
   - `User/Group`: Appropriate user (www-data, nginx, etc.)

3. **Reload systemd:**
   ```bash
   sudo systemctl daemon-reload
   ```

4. **Enable service (auto-start on boot):**
   ```bash
   sudo systemctl enable fastapi
   ```

5. **Start service:**
   ```bash
   sudo systemctl start fastapi
   ```

### Service Management

```bash
# Check status
sudo systemctl status fastapi

# Start service
sudo systemctl start fastapi

# Stop service
sudo systemctl stop fastapi

# Restart service
sudo systemctl restart fastapi

# View logs
sudo journalctl -u fastapi -f

# View recent logs
sudo journalctl -u fastapi -n 100
```

---

## Option 2: Supervisor (Cross-platform)

### Installation

1. **Install supervisor:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install supervisor
   
   # CentOS/RHEL
   sudo yum install supervisor
   ```

2. **Copy configuration:**
   ```bash
   sudo cp docs/deployment/fastapi.supervisor.conf /etc/supervisor/conf.d/fastapi.conf
   ```

3. **Edit configuration:**
   ```bash
   sudo nano /etc/supervisor/conf.d/fastapi.conf
   ```
   
   Update paths:
   - `command`: Path to venv/bin/uvicorn and module path
   - `directory`: Path to Agent_Cellphone_V2_Repository
   - `user/group`: Appropriate user
   - Log file paths

4. **Create log directory:**
   ```bash
   sudo mkdir -p /var/log/fastapi
   sudo chown www-data:www-data /var/log/fastapi
   ```

5. **Reload supervisor:**
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   ```

6. **Start service:**
   ```bash
   sudo supervisorctl start fastapi
   ```

### Service Management

```bash
# Check status
sudo supervisorctl status fastapi

# Start service
sudo supervisorctl start fastapi

# Stop service
sudo supervisorctl stop fastapi

# Restart service
sudo supervisorctl restart fastapi

# View logs
tail -f /var/log/fastapi/access.log
tail -f /var/log/fastapi/error.log

# Reload configuration
sudo supervisorctl reread
sudo supervisorctl update
```

---

## Option 3: Docker (Containerized Deployment)

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  fastapi:
    build: .
    container_name: fastapi
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Docker Commands

```bash
# Build image
docker build -t fastapi:latest .

# Run container
docker run -d -p 8000:8000 --env-file .env fastapi:latest

# Using docker-compose
docker-compose up -d

# View logs
docker logs -f fastapi

# Stop
docker stop fastapi
```

---

## Deployment Script

Use the provided deployment script for automated deployments:

```bash
# Make executable
chmod +x docs/deployment/deploy_fastapi.sh

# Run deployment
./docs/deployment/deploy_fastapi.sh production v1.0.0
```

The script handles:
- Prerequisite checks
- Backup creation
- Code updates
- Dependency installation
- Database migrations
- Pre-deployment checks
- Service restart
- Post-deployment health checks
- Log monitoring

---

## Comparison

| Feature | systemd | Supervisor | Docker |
|---------|---------|------------|--------|
| Platform | Linux only | Cross-platform | Cross-platform |
| Auto-restart | ✅ Yes | ✅ Yes | ✅ Yes |
| Log rotation | ✅ Yes (journald) | ✅ Yes | ⚠️ Manual |
| Resource limits | ✅ Yes | ✅ Yes | ✅ Yes |
| Easy setup | ⚠️ Medium | ✅ Easy | ⚠️ Medium |
| Production ready | ✅ Yes | ✅ Yes | ✅ Yes |
| Container isolation | ❌ No | ❌ No | ✅ Yes |

**Recommendation:** Use systemd for Linux production servers, Supervisor for cross-platform or when systemd is not available, Docker for containerized deployments.

---

## Configuration Notes

### Environment Variables

All process managers should load environment variables from `.env` file:
- systemd: Use `EnvironmentFile` directive
- Supervisor: Load via wrapper script or use `envdir`
- Docker: Use `env_file` in docker-compose or `--env-file` flag

### Logging

Configure log rotation to prevent disk space issues:
- systemd: Configure in `/etc/systemd/journald.conf`
- Supervisor: Use `stdout_logfile_maxbytes` and `stdout_logfile_backups`
- Docker: Configure via logging driver

### Security

- Run service as non-root user (www-data, nginx, etc.)
- Set appropriate file permissions
- Use `PrivateTmp` in systemd for isolation
- Restrict file system access with `ProtectSystem` and `ProtectHome`

---

**Last Updated:** 2025-12-30  
**Status:** ✅ Ready for deployment

