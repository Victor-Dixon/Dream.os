# 🔧 GitHub Integration Setup for Dream.os Agents

## 🎯 Overview
Enable full GitHub API access for automated repository management, issue tracking, and CI/CD setup.

## 📋 Prerequisites
- GitHub account
- Personal Access Token with appropriate permissions

## �� Step-by-Step GitHub Token Setup

### Step 1: Generate GitHub Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: `Dream.os Agent Automation`
4. Expiration: No expiration (or set as preferred)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `user:email` (Access user email)
   - ✅ `read:user` (Read user profile data)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

### Step 2: Configure Dream.os
```bash
cd /home/dream/Development/Dream.os
nano .env
```

Add this line (replace with your real token):
```
GITHUB_TOKEN=ghp_1234567890abcdef1234567890abcdef12345678
```

### Step 3: Test Integration
```bash
cd /home/dream/Development/Dream.os
source venv/bin/activate
python test_github_integration.py
```

Should show:
```
✅ GitHub API integration framework operational
✅ Repository analysis working
✅ Issue creation available
✅ CI/CD setup ready
```

## 🤖 Available GitHub Agent Commands

### Repository Management
```bash
# Analyze repository health
/github analyze Victor-Dixon/AgentTools

# Create professional setup
/github setup

# Setup CI/CD
/github ci Victor-Dixon/MeTuber python
```

### Issue Management
```bash
# Create issue via Discord
/github issue Victor-Dixon/Dream.os "Bug Fix" "Fix agent coordination issue"

# Bulk operations
/github bulk health_check Victor-Dixon/AgentTools Victor-Dixon/Dream.os
```

### Programmatic Access
```python
from tools.github.simple_github_manager import analyze_repo, create_repo_issue

# Analyze repository
result = analyze_repo("Victor-Dixon/AgentTools")

# Create issue
issue = create_repo_issue("Victor-Dixon/Dream.os", "Feature Request", "Add new agent capabilities")
```

## 📊 GitHub Integration Features

### Health Analysis
- Repository score (0-100)
- Recommendations for improvement
- Activity monitoring
- Code quality metrics

### Automation Capabilities
- Issue creation and management
- Pull request handling
- CI/CD workflow setup
- Branch protection rules
- Repository organization

### Bulk Operations
- Multi-repository analysis
- Batch issue creation
- Automated maintenance
- Compliance checking

## 🔒 Security Considerations

### Token Management
- Store token securely in .env (never commit)
- Rotate tokens regularly
- Use minimal required permissions
- Monitor token usage

### API Rate Limits
- GitHub allows 5000 requests/hour for authenticated users
- System automatically handles rate limiting
- Implements exponential backoff for retries

### Access Control
- Configure repository permissions appropriately
- Use organization accounts for team access
- Implement audit logging for all operations

## 🚨 Troubleshooting

### Authentication Errors
```
❌ GitHub API error: 401 Client Error: Unauthorized
```
- Verify token is correct and not expired
- Check token permissions include required scopes
- Ensure token is properly set in .env

### Rate Limit Exceeded
```
❌ GitHub API error: 403 Client Error: rate limit exceeded
```
- Wait for rate limit reset (1 hour)
- Reduce request frequency
- Implement caching for repeated operations

### Repository Access Denied
```
❌ Repository not found or access denied
```
- Verify repository exists and is public
- Check token has access to private repositories
- Confirm correct repository owner/name format

## 📈 Advanced Features

### Webhook Integration
- Automatic issue updates
- CI/CD status notifications
- Repository health alerts
- Agent coordination triggers

### Custom Workflows
- Organization-specific rules
- Automated code review
- Security scanning integration
- Performance monitoring

### Analytics Dashboard
- Repository health trends
- Agent productivity metrics
- Automation success rates
- System performance insights

## 🎯 Integration Testing

### Full System Test
```bash
cd /home/dream/Development/Dream.os
source venv/bin/activate

# Test all components
python -c "
from tools.github.simple_github_manager import get_github_status, analyze_repo
print('GitHub Status:', get_github_status())
print('Test Analysis:', analyze_repo('octocat/Hello-World')[:100])
"
```

### Agent Workflow Test
```bash
# Via Discord (once bot is configured)
/github analyze Victor-Dixon/Dream.os
/github issue Victor-Dixon/AgentTools "Integration Test" "Testing GitHub automation"

# Via CLI
python -m src.services.messaging_cli --message "Test GitHub integration" --broadcast
```

## 📊 Monitoring & Metrics

### Health Dashboard
```bash
# Web interface
curl http://localhost:5000/health

# GitHub integration status
python -c "from tools.github.simple_github_manager import get_github_status; print(get_github_status())"
```

### Performance Metrics
- API response times
- Success/failure rates
- Token usage statistics
- Repository coverage

## 🚀 Production Deployment

### Environment Setup
```bash
# Production .env configuration
cp .env.example .env.production
nano .env.production  # Configure production tokens

# Start production services
export DREAMOS_ENV=production
python main.py --fastapi --discord --background
```

### Scaling Considerations
- Implement Redis for message queuing
- Add load balancing for multiple instances
- Configure monitoring and alerting
- Set up automated backups

### Backup & Recovery
```bash
# Backup configurations
tar -czf dreamos_backup_$(date +%Y%m%d).tar.gz .env config/ agent_workspaces/

# Recovery procedure
tar -xzf dreamos_backup_*.tar.gz
python main.py --restore-config
```

---

**�� With GitHub integration complete, your Dream.os agents can now fully automate repository management, issue tracking, and development workflows!**
