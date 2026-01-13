# 🔧 Discord Bot Error Resolution Guide

**Issue:** Multiple errors encountered when starting Discord bot
**Timestamp:** 2026-01-13 05:24:30
**Errors Identified:**
1. Redis connection failure (`Error 22 connecting to localhost:6379`)
2. Log file rotation PermissionError
3. Asyncio CancelledError (from shutdown)

---

## 🚨 PRIMARY ISSUE: Redis Server Not Running

### Root Cause
The Discord bot system requires Redis for event handling and caching, but Redis server is not running on `localhost:6379`.

### Immediate Solutions

#### Option 1: Start Redis via Docker (Recommended)
```bash
# Check if Docker is running
docker --version

# Start Redis container
docker run -d --name agent-redis -p 6379:6379 redis:7-alpine

# Verify Redis is running
docker ps | grep redis
```

#### Option 2: Enable Redis in Docker Compose
```bash
# Edit docker-compose.yml - uncomment Redis section
# Lines 43-47 in docker-compose.yml

# Start all services including Redis
docker-compose up -d redis

# Verify
docker-compose ps
```

#### Option 3: Install Redis Locally (Windows)
```powershell
# Using Chocolatey (if installed)
choco install redis-64

# Or download from: https://redis.io/download

# Start Redis service
redis-server

# Verify connection
redis-cli ping  # Should respond "PONG"
```

### Configuration Verification
```bash
# Check environment variables
echo $REDIS_URL  # Should be: redis://localhost:6379

# Test connection manually
python -c "
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
try:
    r.ping()
    print('✅ Redis connection successful')
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
"
```

---

## 🔄 SECONDARY ISSUE: Log File Permission Error

### Root Cause
Log file `src/logs/agent_cellphone.log` is locked by another process, preventing log rotation.

### Solutions

#### Option 1: Close Conflicting Processes
```bash
# Find processes using the log file
tasklist | findstr "python"
tasklist | findstr "agent"

# Kill specific processes if needed
taskkill /PID <process_id> /F
```

#### Option 2: Manual Log Rotation
```bash
# Navigate to logs directory
cd src/logs

# Backup current log
copy agent_cellphone.log agent_cellphone.log.backup

# Clear current log
echo. > agent_cellphone.log
```

#### Option 3: Change Log Configuration
```python
# In logging configuration, change to non-rotating handler
# Or use different log file location
LOG_FILE = "src/logs/agent_cellphone_{timestamp}.log"
```

---

## ⚡ TERTIARY ISSUE: Asyncio Cancellation

### Root Cause
Normal shutdown behavior when bot is stopped with Ctrl+C or system signal.

### Assessment
This error is **expected behavior** when stopping the bot. No action required unless it occurs during normal operation.

---

## 🛠️ COMPLETE RESOLUTION STEPS

### Step 1: Start Required Services
```bash
# 1. Start Redis
docker run -d --name agent-redis -p 6379:6379 redis:7-alpine

# 2. Verify Redis connection
docker exec -it agent-redis redis-cli ping

# 3. Check environment
set REDIS_URL=redis://localhost:6379
```

### Step 2: Clear Log File Conflicts
```bash
# 1. Navigate to project root
cd D:\Agent_Cellphone_V2_Repository

# 2. Stop any running Python processes
taskkill /F /IM python.exe

# 3. Clear or backup log file
echo. > src\logs\agent_cellphone.log
```

### Step 3: Restart Discord Bot
```bash
# 1. Ensure environment variables are set
set DISCORD_BOT_TOKEN=your_token_here
set REDIS_URL=redis://localhost:6379

# 2. Start bot
python src/discord_commander/unified_discord_bot.py
```

---

## 🔍 DIAGNOSTIC CHECKLIST

### Pre-Startup Checks
- [ ] Redis server running on localhost:6379
- [ ] Environment variable `REDIS_URL` set correctly
- [ ] Log file not locked by another process
- [ ] Discord bot token configured
- [ ] All Python dependencies installed

### Runtime Health Checks
```bash
# Check Redis connectivity
python -c "import redis; redis.Redis().ping()"

# Check log file permissions
icacls src\logs\agent_cellphone.log

# Verify Discord token
echo %DISCORD_BOT_TOKEN% | head -c 10  # Should show start of token
```

---

## 🚨 PREVENTION MEASURES

### For Future Deployments
1. **Docker Compose Configuration**: Keep Redis enabled in docker-compose.yml
2. **Environment Setup**: Include Redis startup in deployment scripts
3. **Log Rotation**: Implement proper log rotation configuration
4. **Health Checks**: Add startup health checks for required services

### Monitoring Recommendations
1. **Redis Monitoring**: Track Redis memory usage and connections
2. **Log Monitoring**: Monitor log file sizes and rotation
3. **Process Monitoring**: Track running Python processes

---

## 📋 TROUBLESHOOTING SCRIPTS

### Redis Health Check Script
```python
#!/usr/bin/env python3
"""
Redis Health Check for Discord Bot
"""
import redis
import sys

def check_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis: Connected successfully")
        return True
    except redis.ConnectionError as e:
        print(f"❌ Redis: Connection failed - {e}")
        return False
    except Exception as e:
        print(f"❌ Redis: Unexpected error - {e}")
        return False

if __name__ == "__main__":
    success = check_redis()
    sys.exit(0 if success else 1)
```

### Log File Health Check Script
```python
#!/usr/bin/env python3
"""
Log File Health Check for Discord Bot
"""
import os
from pathlib import Path

def check_log_file():
    log_path = Path("src/logs/agent_cellphone.log")

    # Check if file exists
    if not log_path.exists():
        print("✅ Log file: Does not exist (will be created)")
        return True

    # Check permissions
    try:
        with open(log_path, 'a') as f:
            f.write("")  # Test write access
        print("✅ Log file: Write access confirmed")
        return True
    except PermissionError:
        print("❌ Log file: Permission denied")
        return False
    except Exception as e:
        print(f"❌ Log file: Unexpected error - {e}")
        return False

if __name__ == "__main__":
    success = check_log_file()
    sys.exit(0 if success else 1)
```

---

## 📞 SUPPORT CONTACTS

### For Redis Issues
- **Docker Issues**: Check Docker Desktop is running
- **Port Conflicts**: Ensure port 6379 is not used by another service
- **Memory Issues**: Redis may need more memory allocation

### For Log Issues
- **Permission Issues**: Run as Administrator or check file permissions
- **Disk Space**: Ensure sufficient disk space for logs
- **Antivirus**: Check if antivirus is blocking file access

### For Bot Issues
- **Token Issues**: Verify Discord bot token is valid and has correct permissions
- **Rate Limiting**: Check if bot is hitting Discord API rate limits
- **Network Issues**: Verify internet connectivity

---

**Resolution Status:** Issues identified and solutions provided
**Next Steps:** Follow resolution steps above to restore bot functionality
**Prevention:** Implement monitoring and automated health checks</content>
</xai:function_call<parameter name="path">D:\Agent_Cellphone_V2_Repository\docs\troubleshooting\DISCORD_BOT_ERROR_RESOLUTION.md