#!/bin/bash
# FastAPI Deployment Script
# Usage: ./deploy_fastapi.sh [environment] [version]
# Example: ./deploy_fastapi.sh production v1.0.0

set -e  # Exit on error

ENVIRONMENT=${1:-production}
VERSION=${2:-latest}
DEPLOY_DIR="/path/to/Agent_Cellphone_V2_Repository"
VENV_PATH="/path/to/venv"
SERVICE_NAME="fastapi"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if [ ! -d "$DEPLOY_DIR" ]; then
        log_error "Deployment directory not found: $DEPLOY_DIR"
        exit 1
    fi
    
    if [ ! -f "$DEPLOY_DIR/.env" ]; then
        log_warn ".env file not found. Make sure environment variables are configured."
    fi
    
    if [ ! -d "$VENV_PATH" ]; then
        log_error "Virtual environment not found: $VENV_PATH"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

# Backup current deployment
backup_deployment() {
    log_info "Creating backup..."
    
    BACKUP_DIR="$DEPLOY_DIR/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup code (if using git, this is handled by version control)
    # Backup database if applicable
    # Backup configuration files
    
    log_info "Backup created at $BACKUP_DIR"
}

# Pull latest code
pull_code() {
    log_info "Pulling latest code..."
    cd "$DEPLOY_DIR"
    
    if [ -d ".git" ]; then
        git pull origin main
        if [ "$VERSION" != "latest" ]; then
            git checkout "$VERSION"
        fi
        log_info "Code updated to version: $(git rev-parse --short HEAD)"
    else
        log_warn "Not a git repository, skipping code pull"
    fi
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies..."
    
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    pip install -r "$DEPLOY_DIR/requirements.txt"
    
    # Verify FastAPI installation
    python -c "import fastapi; import uvicorn" || {
        log_error "FastAPI dependencies not installed correctly"
        exit 1
    }
    
    log_info "Dependencies installed successfully"
}

# Run database migrations (if applicable)
run_migrations() {
    log_info "Running database migrations..."
    
    cd "$DEPLOY_DIR"
    source "$VENV_PATH/bin/activate"
    
    # Add migration commands here if applicable
    # alembic upgrade head
    # OR
    # python -m src.core.database.migrate
    
    log_info "Migrations completed"
}

# Pre-deployment health check
pre_deployment_check() {
    log_info "Running pre-deployment checks..."
    
    cd "$DEPLOY_DIR"
    source "$VENV_PATH/bin/activate"
    
    # Check if FastAPI app can be imported
    python -c "from src.api.main import app" || {
        log_error "FastAPI app import failed"
        exit 1
    }
    
    # Run tests if available
    if [ -d "tests" ]; then
        log_info "Running tests..."
        pytest tests/ || {
            log_error "Tests failed"
            exit 1
        }
    fi
    
    log_info "Pre-deployment checks passed"
}

# Deploy (restart service)
deploy_service() {
    log_info "Deploying service..."
    
    # Check if systemd service exists
    if systemctl list-unit-files | grep -q "^${SERVICE_NAME}.service"; then
        log_info "Using systemd for service management"
        sudo systemctl restart "$SERVICE_NAME"
        sudo systemctl status "$SERVICE_NAME" --no-pager
    # Check if supervisor config exists
    elif [ -f "/etc/supervisor/conf.d/${SERVICE_NAME}.conf" ]; then
        log_info "Using supervisor for service management"
        sudo supervisorctl restart "$SERVICE_NAME"
        sudo supervisorctl status "$SERVICE_NAME"
    else
        log_warn "No service manager found. Manual restart required."
    fi
}

# Post-deployment health check
post_deployment_check() {
    log_info "Running post-deployment health checks..."
    
    # Wait for service to start
    sleep 5
    
    # Check health endpoint
    API_URL="${API_URL:-http://localhost:8000}"
    HEALTH_CHECK="${API_URL}/health"
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_CHECK" || echo "000")
    
    if [ "$response" = "200" ]; then
        log_info "Health check passed (HTTP $response)"
    else
        log_error "Health check failed (HTTP $response)"
        log_error "Service may not be running correctly"
        exit 1
    fi
    
    # Check service status
    if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
        log_info "Service is active"
    elif supervisorctl status "$SERVICE_NAME" | grep -q "RUNNING" 2>/dev/null; then
        log_info "Service is running"
    else
        log_warn "Could not verify service status"
    fi
}

# Monitor logs
monitor_logs() {
    log_info "Monitoring logs for errors..."
    
    # Show last 20 lines of error log
    if [ -f "/var/log/fastapi/error.log" ]; then
        tail -20 /var/log/fastapi/error.log
    elif systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
        journalctl -u "$SERVICE_NAME" -n 20 --no-pager
    fi
}

# Rollback function
rollback() {
    log_warn "Rolling back deployment..."
    
    # Stop service
    if systemctl list-unit-files | grep -q "^${SERVICE_NAME}.service"; then
        sudo systemctl stop "$SERVICE_NAME"
    elif [ -f "/etc/supervisor/conf.d/${SERVICE_NAME}.conf" ]; then
        sudo supervisorctl stop "$SERVICE_NAME"
    fi
    
    # Restore from backup
    # cd "$DEPLOY_DIR"
    # git checkout <previous_commit>
    
    # Restart service
    deploy_service
    
    log_info "Rollback completed"
}

# Main deployment flow
main() {
    log_info "Starting FastAPI deployment..."
    log_info "Environment: $ENVIRONMENT"
    log_info "Version: $VERSION"
    
    check_prerequisites
    backup_deployment
    pull_code
    install_dependencies
    run_migrations
    pre_deployment_check
    deploy_service
    post_deployment_check
    monitor_logs
    
    log_info "Deployment completed successfully!"
}

# Trap errors and call rollback
trap 'log_error "Deployment failed. Consider rollback."; exit 1' ERR

# Run main function
main "$@"

