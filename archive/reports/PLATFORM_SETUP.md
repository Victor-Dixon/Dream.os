# 🚀 Platform-Specific Setup Guides

**Complete platform guides for dream.os setup on Windows, macOS, and Linux**

[![Windows](https://img.shields.io/badge/Windows-10+-blue)](https://docs.microsoft.com/en-us/windows/)
[![macOS](https://img.shields.io/badge/macOS-10.15+-silver)](https://www.apple.com/macos/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-18.04+-orange)](https://ubuntu.com/)
[![Docker](https://img.shields.io/badge/Docker-Any-blue)](https://docker.com)

---

## 📋 Quick Platform Check

**What's your platform?**

```bash
# Run this command to check your system:
python scripts/post_clone_check.py
```

This will automatically detect your platform and validate compatibility.

---

## 🐳 Universal Docker Setup (Recommended)

**Works on Windows, macOS, and Linux - No platform differences!**

### Prerequisites
- [Docker Desktop](https://docker.com/get-started) installed and running
- 4GB RAM available
- 10GB disk space

### One-Command Setup
```bash
# Clone and setup in one command
git clone https://github.com/your-org/dream-os.git
cd dream-os
python setup.py --docker
```

### Manual Docker Setup
```bash
# 1. Clone repository
git clone https://github.com/your-org/dream-os.git
cd dream-os

# 2. Run validation
python scripts/post_clone_check.py

# 3. Configure environment
python setup_wizard.py

# 4. Install with Docker
./install.sh --docker

# 5. Start services
docker-compose up -d

# 6. Check status
docker-compose ps
```

### Docker Access Points
- **Web Dashboard**: http://localhost:5000
- **API Documentation**: http://localhost:8001/docs
- **Grafana Monitoring**: http://localhost:3000 (admin/admin123)

---

## 🪟 Windows Setup

### Native Python Installation

#### Prerequisites
- Windows 10 or 11
- Python 3.11+ from [python.org](https://python.org)
- Git for Windows

#### Installation Steps
```batch
# 1. Clone repository
git clone https://github.com/your-org/dream-os.git
cd dream-os

# 2. Run validation
python scripts/post_clone_check.py

# 3. Install dependencies
install.bat

# 4. Configure environment
python setup_wizard.py

# 5. Start services
python main.py --background

# 6. Check status
python main.py --status
```

### Windows Troubleshooting

#### Common Issues

**Python not found**
```batch
# Check Python installation
python --version

# If not found, install from python.org
# Make sure to check "Add Python to PATH"
```

**Permission denied**
```batch
# Run PowerShell as Administrator
# Or use: python main.py --background
```

**Port conflicts**
```batch
# Check what's using ports
netstat -ano | findstr :5000
netstat -ano | findstr :8001

# Kill process if needed
taskkill /PID <process_id> /F
```

**Firewall blocking**
```batch
# Allow Python through firewall
# Windows Security > Firewall & network protection > Allow an app
```

---

## 🍎 macOS Setup

### Native Python Installation

#### Prerequisites
- macOS 10.15 (Catalina) or later
- Xcode Command Line Tools: `xcode-select --install`
- Python 3.11+ (use [pyenv](https://github.com/pyenv/pyenv) recommended)

#### Installation Steps
```bash
# 1. Install Xcode tools (if not already)
xcode-select --install

# 2. Install Python 3.11+ (recommended: pyenv)
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

pyenv install 3.11.6
pyenv global 3.11.6

# 3. Clone and setup
git clone https://github.com/your-org/dream-os.git
cd dream-os

# 4. Run validation
python scripts/post_clone_check.py

# 5. Install dependencies
./install.sh

# 6. Configure environment
python setup_wizard.py

# 7. Start services
python main.py --background

# 8. Check status
python main.py --status
```

### macOS Troubleshooting

#### Common Issues

**Python version conflicts**
```bash
# Check Python version
python --version
python3 --version

# Use pyenv to manage versions
pyenv versions
pyenv global 3.11.6
```

**Permission denied on install**
```bash
# Use sudo for system Python (not recommended)
# Better: use pyenv for user-space Python
```

**Port conflicts**
```bash
# Check ports
lsof -i :5000
lsof -i :8001

# Kill process
kill -9 <process_id>
```

**Homebrew conflicts**
```bash
# If you have Homebrew Python conflicts
brew unlink python
# Use pyenv instead
```

---

## 🐧 Linux Setup

### Ubuntu/Debian Installation

#### Prerequisites
- Ubuntu 18.04+ or Debian 10+
- sudo access

#### Installation Steps
```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.11+
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# 3. Clone repository
git clone https://github.com/your-org/dream-os.git
cd dream-os

# 4. Run validation
python scripts/post_clone_check.py

# 5. Install dependencies
./install.sh

# 6. Configure environment
python setup_wizard.py

# 7. Start services
python main.py --background

# 8. Check status
python main.py --status
```

### CentOS/RHEL Installation

#### Prerequisites
- CentOS 7+ or RHEL 7+
- sudo access

#### Installation Steps
```bash
# 1. Install Python 3.11+
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel
wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz
tar xzf Python-3.11.6.tgz
cd Python-3.11.6
./configure --enable-optimizations
sudo make altinstall

# 2. Clone repository
git clone https://github.com/your-org/dream-os.git
cd dream-os

# 3. Run validation
python3.11 scripts/post_clone_check.py

# 4. Install dependencies
./install.sh

# 5. Configure environment
python3.11 setup_wizard.py

# 6. Start services
python3.11 main.py --background

# 7. Check status
python3.11 main.py --status
```

### Arch Linux Installation

#### Prerequisites
- Arch Linux (any recent version)

#### Installation Steps
```bash
# 1. Update system
sudo pacman -Syu

# 2. Install Python 3.11+
sudo pacman -S python python-pip

# 3. Clone repository
git clone https://github.com/your-org/dream-os.git
cd dream-os

# 4. Run validation
python scripts/post_clone_check.py

# 5. Install dependencies
./install.sh

# 6. Configure environment
python setup_wizard.py

# 7. Start services
python main.py --background

# 8. Check status
python main.py --status
```

### Linux Troubleshooting

#### Common Issues

**Python headers missing**
```bash
# Ubuntu/Debian
sudo apt install python3.11-dev

# CentOS/RHEL
sudo yum install python3-devel
```

**Permission denied**
```bash
# Check permissions
ls -la

# Fix permissions if needed
chmod +x install.sh
chmod +x scripts/*.py
```

**Port conflicts**
```bash
# Check ports
sudo netstat -tulpn | grep :5000
sudo netstat -tulpn | grep :8001

# Kill process
sudo kill -9 <process_id>
```

**Firewall blocking**
```bash
# Ubuntu/Debian ufw
sudo ufw allow 5000
sudo ufw allow 8001

# CentOS/RHEL firewalld
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --reload
```

---

## 🔧 Advanced Configuration

### Environment Variables

After setup, you can customize behavior with these environment variables:

```bash
# Performance tuning
WEB_WORKERS=4
API_TIMEOUT=30
LOG_LEVEL=INFO

# Service ports
WEB_PORT=5000
FASTAPI_PORT=8001

# Database settings
DB_POOL_SIZE=10
DB_CONNECTION_TIMEOUT=10
```

### Service Configuration

Edit `config/` files for advanced service configuration:

- `config/prometheus.yml` - Monitoring configuration
- `config/kong/kong.yml` - API gateway configuration
- `config/postgres.conf` - Database optimization
- `config/redis.conf` - Caching configuration

---

## 🐛 Platform-Specific Issues

### Windows Issues

**WSL Performance**
```batch
# Use native Windows Python instead of WSL
# WSL can have performance issues with Docker
```

**Antivirus Interference**
```batch
# Add dream-os to antivirus exclusions
# Some antivirus blocks Python network operations
```

### macOS Issues

**Gatekeeper Blocking**
```bash
# Allow app execution
sudo spctl --master-disable
# Re-enable after setup: sudo spctl --master-enable
```

**Python from App Store**
```bash
# Avoid App Store Python - use pyenv instead
# App Store Python has permission restrictions
```

### Linux Issues

**SELinux Blocking**
```bash
# Check SELinux status
sestatus

# Temporarily disable if needed
sudo setenforce 0
# Re-enable: sudo setenforce 1
```

**Systemd Conflicts**
```bash
# Check for systemd service conflicts
sudo systemctl list-units --type=service | grep dream
```

---

## 📞 Getting Help

### Community Support

- **Discord**: Join our community server
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check docs/ for detailed guides

### Diagnostic Commands

```bash
# Run full system diagnosis
python scripts/post_clone_check.py

# Check service health
python scripts/health_check.py --check

# View detailed logs
tail -f logs/app.log

# Validate configuration
python setup_wizard.py --validate
```

### Emergency Recovery

If setup fails completely:

```bash
# Clean restart
python main.py --kill
rm -rf logs/* pids/* temp/*
python setup.py --validate
```

---

## 🎯 Next Steps

After successful setup:

1. **Explore the Dashboard**: http://localhost:5000
2. **Read the API Docs**: http://localhost:8001/docs
3. **Configure Discord Bot**: Add your bot token
4. **Join the Community**: Get help and share your setup
5. **Start Building**: Check docs/guides/ for tutorials

---

**🐝 Happy building with dream.os!**

*Setup time: 5-15 minutes depending on platform and method*