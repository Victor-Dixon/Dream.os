#!/bin/bash
# dream.os - Installation Script
# ========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."

    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="windows"
    else
        log_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi

    # Check Python version
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3.11+ is required but not found"
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ "$(printf '%s\n' "$PYTHON_VERSION" "3.11" | sort -V | head -n1)" != "3.11" ]]; then
        log_error "Python 3.11+ is required, found $PYTHON_VERSION"
        exit 1
    fi

    # Check Docker (optional but recommended)
    if command -v docker &> /dev/null; then
        DOCKER_AVAILABLE=true
        log_info "Docker found - containerized deployment available"
    else
        DOCKER_AVAILABLE=false
        log_warning "Docker not found - will install in standalone mode"
    fi

    log_success "System requirements check passed"
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."

    if [[ -f "requirements.txt" ]]; then
        pip3 install -r requirements.txt
        log_success "Python dependencies installed"
    else
        log_error "requirements.txt not found"
        exit 1
    fi
}

# Setup environment configuration
setup_environment() {
    log_info "Setting up environment configuration..."

    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        log_warning ".env file created from template. Please edit with your configuration."
        echo ""
        echo "Please edit .env file with your:"
        echo "  - Discord bot token"
        echo "  - Twitch credentials"
        echo "  - Database settings"
        echo "  - API keys"
        echo ""
    else
        log_info ".env file already exists"
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."

    directories=(
        "agent_workspaces"
        "logs"
        "runtime"
        "pids"
        "data"
        "cache"
        "temp"
    )

    for dir in "${directories[@]}"; do
        if [[ ! -d "$dir" ]]; then
            mkdir -p "$dir"
            log_info "Created directory: $dir"
        fi
    done

    log_success "Directories created"
}

# Initialize agent workspaces
initialize_agents() {
    log_info "Initializing agent workspaces..."

    # Create agent registry if it doesn't exist
    if [[ ! -f "agent_workspaces/agent_registry.json" ]]; then
        python3 scripts/agent_onboarding.py --create-registry
        log_success "Agent registry created"
    fi

    # Initialize agent workspaces
    for i in {1..8}; do
        agent_dir="agent_workspaces/Agent-${i}"
        if [[ ! -d "$agent_dir" ]]; then
            mkdir -p "$agent_dir"
            # Initialize basic agent files
            echo '{"agent_id": "Agent-'"$i"'", "status": "INACTIVE"}' > "$agent_dir/status.json"
            mkdir -p "$agent_dir/inbox" "$agent_dir/archive"
            log_info "Initialized Agent-$i workspace"
        fi
    done

    log_success "Agent workspaces initialized"
}

# Setup Docker (if available and chosen)
setup_docker() {
    if [[ "$DOCKER_AVAILABLE" == true && "$INSTALL_MODE" == "docker" ]]; then
        log_info "Setting up Docker deployment..."

        # Check if docker-compose is available
        if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
            log_error "docker-compose is required for Docker deployment"
            exit 1
        fi

        # Create .env for Docker if needed
        if [[ ! -f ".env.docker" ]]; then
            cat > .env.docker << EOF
# Docker-specific environment variables
COMPOSE_PROJECT_NAME=agent-cellphone-v2
POSTGRES_PASSWORD=agent_password_secure
GRAFANA_PASSWORD=admin
EOF
            log_info ".env.docker created"
        fi

        log_success "Docker setup completed"
    fi
}

# Main installation function
main() {
    echo "🚀 Agent Cellphone V2 Installation"
    echo "=================================="

    # Parse command line arguments
    INSTALL_MODE="standalone"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --docker)
                INSTALL_MODE="docker"
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [--docker] [--help]"
                echo ""
                echo "Options:"
                echo "  --docker    Install using Docker (recommended)"
                echo "  --help      Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    check_requirements
    create_directories
    setup_environment

    if [[ "$INSTALL_MODE" == "docker" ]]; then
        setup_docker
    else
        install_python_deps
        initialize_agents
    fi

    echo ""
    log_success "Installation completed!"
    echo ""
    echo "Next steps:"
    if [[ "$INSTALL_MODE" == "docker" ]]; then
        echo "  1. Edit .env.docker with your configuration"
        echo "  2. Run: docker-compose up -d"
        echo "  3. Check status: docker-compose ps"
    else
        echo "  1. Edit .env with your configuration"
        echo "  2. Run: python main.py --status"
        echo "  3. Start services: python main.py --background"
    fi
    echo ""
    echo "📚 Documentation: https://docs.agent-cellphone-v2.com"
}

# Run main function
main "$@"