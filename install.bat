@echo off
REM Agent Cellphone V2 - Windows Installation Script
REM ================================================

setlocal enabledelayedexpansion

REM Colors for Windows (limited support)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

REM Logging functions
:log_info
echo [INFO] %~1
goto :eof

:log_success
echo [SUCCESS] %~1
goto :eof

:log_warning
echo [WARNING] %~1
goto :eof

:log_error
echo [ERROR] %~1
goto :eof

REM Check system requirements
:check_requirements
call :log_info "Checking system requirements..."

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Python is required but not found"
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% lss 3 (
    call :log_error "Python 3.11+ is required, found %PYTHON_VERSION%"
    pause
    exit /b 1
)

if %PYTHON_MINOR% lss 11 (
    call :log_error "Python 3.11+ is required, found %PYTHON_VERSION%"
    pause
    exit /b 1
)

REM Check Docker (optional)
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_AVAILABLE=true
    call :log_info "Docker found - containerized deployment available"
) else (
    set DOCKER_AVAILABLE=false
    call :log_warning "Docker not found - will install in standalone mode"
)

call :log_success "System requirements check passed"
goto :eof

REM Install Python dependencies
:install_python_deps
call :log_info "Installing Python dependencies..."

if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        call :log_error "Failed to install Python dependencies"
        pause
        exit /b 1
    )
    call :log_success "Python dependencies installed"
) else (
    call :log_error "requirements.txt not found"
    pause
    exit /b 1
)
goto :eof

REM Setup environment configuration
:setup_environment
call :log_info "Setting up environment configuration..."

if not exist .env (
    if exist .env.example (
        copy .env.example .env
        call :log_warning ".env file created from template. Please edit with your configuration."
        echo.
        echo Please edit .env file with your:
        echo   - Discord bot token
        echo   - Twitch credentials
        echo   - Database settings
        echo   - API keys
        echo.
    ) else (
        call :log_warning ".env.example not found, creating basic .env template"
        echo # Agent Cellphone V2 Configuration > .env
        echo # Please fill in your configuration values >> .env
        echo. >> .env
        echo # Discord Bot >> .env
        echo DISCORD_BOT_TOKEN=your_discord_token_here >> .env
        echo. >> .env
        echo # Twitch Bot >> .env
        echo TWITCH_CHANNEL=your_channel >> .env
        echo TWITCH_ACCESS_TOKEN=oauth:your_twitch_token >> .env
    )
) else (
    call :log_info ".env file already exists"
)
goto :eof

REM Create necessary directories
:create_directories
call :log_info "Creating necessary directories..."

set "directories=agent_workspaces logs runtime pids data cache temp"

for %%d in (%directories%) do (
    if not exist "%%d" (
        mkdir "%%d" 2>nul
        call :log_info "Created directory: %%d"
    )
)

call :log_success "Directories created"
goto :eof

REM Initialize agent workspaces
:initialize_agents
call :log_info "Initializing agent workspaces..."

if not exist "agent_workspaces\agent_registry.json" (
    python scripts\agent_onboarding.py --create-registry
    if errorlevel 1 (
        call :log_warning "Failed to create agent registry, continuing..."
    ) else (
        call :log_success "Agent registry created"
    )
)

for /l %%i in (1,1,8) do (
    set "agent_dir=agent_workspaces\Agent-%%i"
    if not exist "!agent_dir!" (
        mkdir "!agent_dir!" 2>nul
        echo {"agent_id": "Agent-%%i", "status": "INACTIVE"} > "!agent_dir!\status.json"
        mkdir "!agent_dir!\inbox" 2>nul
        mkdir "!agent_dir!\archive" 2>nul
        call :log_info "Initialized Agent-%%i workspace"
    )
)

call :log_success "Agent workspaces initialized"
goto :eof

REM Setup Docker (if available and chosen)
:setup_docker
if "%DOCKER_AVAILABLE%"=="true" if "%INSTALL_MODE%"=="docker" (
    call :log_info "Setting up Docker deployment..."

    REM Check if docker-compose is available
    docker-compose --version >nul 2>&1
    if errorlevel 1 (
        REM Try new Docker Compose syntax
        docker compose version >nul 2>&1
        if errorlevel 1 (
            call :log_error "docker-compose is required for Docker deployment"
            call :log_info "Please install Docker Desktop from https://docker.com"
            pause
            exit /b 1
        )
    )

    REM Create .env for Docker if needed
    if not exist ".env.docker" (
        echo # Docker-specific environment variables > .env.docker
        echo COMPOSE_PROJECT_NAME=agent-cellphone-v2 >> .env.docker
        echo POSTGRES_PASSWORD=agent_password_secure >> .env.docker
        echo GRAFANA_PASSWORD=admin >> .env.docker
        call :log_info ".env.docker created"
    )

    call :log_success "Docker setup completed"
)
goto :eof

REM Main installation function
:main
echo.
echo ================================================
echo   Agent Cellphone V2 - Windows Installation
echo ================================================
echo.

REM Parse command line arguments
set "INSTALL_MODE=standalone"

if "%1"=="--docker" (
    set "INSTALL_MODE=docker"
) else if "%1"=="--help" (
    echo Usage: %0 [--docker] [--help]
    echo.
    echo Options:
    echo   --docker    Install using Docker (recommended)
    echo   --help      Show this help message
    goto :eof
)

call :check_requirements
call :create_directories
call :setup_environment

if "%INSTALL_MODE%"=="docker" (
    call :setup_docker
) else (
    call :install_python_deps
    call :initialize_agents
)

echo.
call :log_success "Installation completed!"
echo.
echo Next steps:
if "%INSTALL_MODE%"=="docker" (
    echo   1. Edit .env.docker with your configuration
    echo   2. Run: docker-compose up -d
    echo   3. Check status: docker-compose ps
) else (
    echo   1. Edit .env with your configuration
    echo   2. Run: python main.py --status
    echo   3. Start services: python main.py --background
)
echo.
echo Documentation: https://docs.agent-cellphone-v2.com
echo.
pause
goto :eof

REM Run main function
call :main %*