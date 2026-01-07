# 🚀 Production Deployment Guide for Dream.os

## 🎯 Overview
Deploy Dream.os to production with full agent orchestration, Discord integration, and GitHub automation.

## 📋 Production Checklist

### ✅ Completed Setup
- [x] Dream.os cloned and configured
- [x] Linux compatibility achieved
- [x] Agent messaging system operational
- [x] GitHub integration framework ready
- [x] Web interface running
- [ ] Discord bot configured
- [ ] GitHub tokens set
- [ ] Production environment configured

### 🔧 Production Configuration

#### 1. Environment Setup
```bash
cd /home/dream/Development/Dream.os

# Create production environment
cp .env .env.production
nano .env.production
```

Add production configuration:
```bash
# Production Environment
DREAMOS_ENV=production
LOG_LEVEL=WARNING
DEBUG_MODE=false

# Discord Bot (Required for agent communication)
DISCORD_BOT_TOKEN=your_production_discord_token

# GitHub Integration (Required for automation)
GITHUB_TOKEN=your_github_personal_access_token

# Database (Optional - uses SQLite by default)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dreamos_prod
DB_USER=dreamos
DB_PASSWORD=secure_password

# Web Interface
WEB_HOST=0.0.0.0
WEB_PORT=8000
SECRET_KEY=your_secure_random_key

# Security
ENCRYPTION_KEY=your_encryption_key
API_SECRET_KEY=your_api_key
```

#### 2. Service Configuration
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib redis-server nginx

# Create database
sudo -u postgres createdb dreamos_prod
sudo -u postgres createuser dreamos
sudo -u postgres psql -c "ALTER USER dreamos PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dreamos_prod TO dreamos;"
```

#### 3. SSL/TLS Setup (Recommended)
```bash
# Get SSL certificate (Let's Encrypt example)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com

# Configure HTTPS in nginx
sudo nano /etc/nginx/sites-available/dreamos
```

#### 4. Systemd Service Setup
```bash
# Create systemd service
sudo nano /etc/systemd/system/dreamos.service
```

Add service configuration:
```ini
[Unit]
Description=Dream.os AI Agent Orchestration System
After=network.target postgresql.service redis-server.service

[Service]
Type=simple
User=dream
Group=dream
WorkingDirectory=/home/dream/Development/Dream.os
Environment=DREAMOS_ENV=production
EnvironmentFile=/home/dream/Development/Dream.os/.env.production
ExecStart=/home/dream/Development/Dream.os/venv/bin/python main.py --fastapi --discord --background
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable dreamos
sudo systemctl start dreamos
sudo systemctl status dreamos
```

## 📊 Monitoring & Observability

### Health Checks
```bash
# System health
curl https://yourdomain.com/health

# Service status
sudo systemctl status dreamos

# Logs
sudo journalctl -u dreamos -f
```

### Performance Monitoring
```bash
# Install monitoring tools
sudo apt-get install htop iotop sysstat

# Monitor system resources
htop
iostat -x 1
free -h
```

### Log Aggregation
```bash
# View application logs
tail -f logs/*.log

# System logs
sudo journalctl -u dreamos --since "1 hour ago"

# Error monitoring
grep -r "ERROR" logs/ --include="*.log"
```

## 🔒 Security Hardening

### Network Security
```bash
# Configure firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000  # Web interface

# SSH hardening
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no
# Set: PasswordAuthentication no
# Set: AllowUsers your_username

sudo systemctl restart sshd
```

### Application Security
```bash
# Environment variables
export SECRET_KEY=$(openssl rand -hex 32)
export ENCRYPTION_KEY=$(openssl rand -hex 32)

# File permissions
chmod 600 .env.production
chmod 700 agent_workspaces/
chmod 755 logs/
```

### Backup Strategy
```bash
# Create backup script
nano backup_dreamos.sh
chmod +x backup_dreamos.sh
```

Backup script:
```bash
#!/bin/bash
BACKUP_DIR="/home/dream/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump dreamos_prod > $BACKUP_DIR/dreamos_db_$DATE.sql

# Backup configurations
tar -czf $BACKUP_DIR/dreamos_config_$DATE.tar.gz .env.production config/

# Backup agent workspaces
tar -czf $BACKUP_DIR/dreamos_workspaces_$DATE.tar.gz agent_workspaces/

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -o -name "*.sql" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Add to crontab:
```bash
crontab -e
# Add: 0 2 * * * /home/dream/Development/Dream.os/backup_dreamos.sh
```

## 🚀 Scaling & Performance

### Horizontal Scaling
```bash
# Load balancer setup (nginx example)
sudo nano /etc/nginx/sites-available/dreamos_lb

upstream dreamos_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://dreamos_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Database Optimization
```bash
# PostgreSQL tuning
sudo nano /etc/postgresql/13/main/postgresql.conf
# Adjust: shared_buffers = 256MB
# Adjust: work_mem = 4MB
# Adjust: maintenance_work_mem = 64MB

sudo systemctl restart postgresql
```

### Caching Setup
```bash
# Redis configuration
sudo nano /etc/redis/redis.conf
# Set: maxmemory 256mb
# Set: maxmemory-policy allkeys-lru

sudo systemctl restart redis-server
```

## 📈 Maintenance Procedures

### Regular Updates
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade

# Update Dream.os
cd /home/dream/Development/Dream.os
git pull origin linux-branch
source venv/bin/activate
pip install -r requirements.txt

# Restart services
sudo systemctl restart dreamos
```

### Troubleshooting Common Issues

#### Service Won't Start
```bash
# Check logs
sudo journalctl -u dreamos -n 50

# Check dependencies
python -c "import discord, fastapi, psutil; print('Dependencies OK')"

# Manual start for debugging
source venv/bin/activate
python main.py --status
```

#### Database Connection Issues
```bash
# Test database connection
sudo -u postgres psql -d dreamos_prod -c "SELECT version();"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-13-main.log
```

#### High Memory Usage
```bash
# Monitor memory
ps aux --sort=-%mem | head

# Restart services
sudo systemctl restart dreamos

# Check for memory leaks
python -c "import tracemalloc; tracemalloc.start(); # Add monitoring code"
```

## 🎯 Success Metrics

### System Health Indicators
- ✅ All services running (FastAPI, Discord, Message Queue)
- ✅ Agent communication working (8-agent swarm)
- ✅ GitHub integration operational
- ✅ Web interface responsive
- ✅ Database connections stable

### Performance Benchmarks
- Response time < 500ms for web requests
- Agent message delivery < 2 seconds
- GitHub API calls < 1000/hour sustained
- Memory usage < 1GB per service
- CPU usage < 50% sustained

### Business Metrics
- Agent coordination successful rate > 95%
- Automated tasks completion rate > 90%
- System uptime > 99.5%
- User satisfaction scores > 4.5/5

## 🚨 Emergency Procedures

### Service Outage Response
1. Check system status: `sudo systemctl status dreamos`
2. Review logs: `sudo journalctl -u dreamos --since "1 hour ago"`
3. Restart services: `sudo systemctl restart dreamos`
4. If restart fails, check dependencies and configuration
5. Contact system administrator if issue persists

### Data Recovery
1. Stop services: `sudo systemctl stop dreamos`
2. Restore from backup: `tar -xzf /home/dream/backups/dreamos_*_latest.tar.gz`
3. Restart services: `sudo systemctl start dreamos`
4. Verify data integrity
5. Update monitoring alerts

### Security Incident Response
1. Isolate affected systems
2. Change all credentials and tokens
3. Review access logs for suspicious activity
4. Apply security patches
5. Restore from clean backup if compromised

---

## 🎉 Production Deployment Complete!

**Your Dream.os AI agent orchestration system is now production-ready with:**

- ✅ **High Availability**: Systemd service management
- ✅ **Security**: SSL/TLS, firewall, secure configurations
- ✅ **Monitoring**: Comprehensive logging and health checks
- ✅ **Scalability**: Load balancing and performance optimization
- ✅ **Reliability**: Backup/recovery and disaster recovery procedures
- ✅ **Maintenance**: Automated updates and troubleshooting guides

**🚀 Your AI agent ecosystem is now enterprise-ready!**
