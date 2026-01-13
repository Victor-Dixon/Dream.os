#!/usr/bin/env python3
"""
Environment Manager - Clean up .env and create env.example
"""

import os
from pathlib import Path

def main():
    # Read the .env file
    env_file = Path('.env')
    if not env_file.exists():
        print('❌ .env file not found')
        return

    print('✅ Found .env file')
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    print(f'📊 .env file has {len(lines)} lines')

    # Parse the variables
    variables = {}
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                key, value = parts
                variables[key.strip()] = value.strip()

    print(f'📋 Found {len(variables)} environment variables')

    # Create PowerShell commands to set variables
    print('\n🔧 PowerShell commands to set environment variables:')
    print('# Copy and paste these commands in PowerShell to set all environment variables')
    for key, value in variables.items():
        if value and value not in ['your_discord_bot_token_here', 'your_twitch_token', 'your_channel', 'your_openai_key', 'change_this_in_production', 'admin123', 'dev_secret_change_in_production', 'prod_secret_change_in_production']:
            print(f'$env:{key} = "{value}"')
        else:
            print(f'# $env:{key} = "YOUR_{key.upper()}_HERE"  # TODO: Set this value')

    # Create env.example
    print('\n📝 Creating env.example file...')
    example_content = '''# =============================================================================
# Agent Cellphone V2 - Environment Configuration
# =============================================================================
#
# Copy this file to .env and fill in your actual values
# IMPORTANT: Never commit .env to version control (it contains secrets)
#
# =============================================================================

# Discord Bot Configuration (REQUIRED)
DISCORD_BOT_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_server_id_here

# Twitch Bot Configuration (OPTIONAL)
TWITCH_CHANNEL=your_channel_name
TWITCH_ACCESS_TOKEN=oauth:your_oauth_token
TWITCH_BOT_USERNAME=your_bot_username

# OpenAI API Configuration (OPTIONAL)
OPENAI_API_KEY=your_openai_api_key

# Docker Configuration
COMPOSE_PROJECT_NAME=dream-os
POSTGRES_PASSWORD=change_this_in_production
GRAFANA_PASSWORD=admin123

# Environment Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG_MODE=false

# Web Server Settings
WEB_HOST=127.0.0.1
WEB_PORT=5000
WEB_WORKERS=4

# API Settings
API_TIMEOUT=30
API_RATE_LIMIT=100

# Database Settings
DB_CONNECTION_TIMEOUT=10
DB_POOL_SIZE=10

# File Paths
LOG_DIRECTORY=logs
CONFIG_DIRECTORY=config
DATA_DIRECTORY=data
CACHE_DIRECTORY=cache

# Performance Settings
SLOW_QUERY_THRESHOLD=1.0
MEMORY_THRESHOLD=100

# Security Settings
FLASK_DEV_SECRET_KEY=dev_secret_change_in_production
FLASK_PROD_SECRET_KEY=prod_secret_change_in_production

# Agent System Configuration
AGENT_COUNT=8
CAPTAIN_ID=Agent-4
DEFAULT_MODE=pyautogui

# Browser Automation
GPT_URL=https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager
MAX_SCRAPE_RETRIES=3

# Test Configuration
COVERAGE_THRESHOLD=80.0
TEST_FAILURE_THRESHOLD=0

# Advanced Timeouts
SCRAPE_TIMEOUT=30.0
RESPONSE_WAIT_TIMEOUT=120.0
SMOKE_TEST_TIMEOUT=60
UNIT_TEST_TIMEOUT=120
INTEGRATION_TEST_TIMEOUT=300

# File Patterns
ARCHITECTURE_FILES=\\.(py|js|ts|java|cpp|h|md)$
TEST_FILES=(test|spec)\\.(py|js|ts|java)$

# Performance Targets
RESPONSE_TIME_TARGET=100.0
THROUGHPUT_TARGET=1000.0
LATENCY_TARGET=50.0

# Advanced Security Keys
PORTAL_SECRET_KEY=
PORTAL_SESSION_SECRET=
HEALTH_MONITOR_SECRET_KEY=

# Twitch Advanced Settings
TWITCH_ADMIN_USERS=
TWITCH_EVENTSUB_WEBHOOK_SECRET=

# Advanced Logging
LOG_SLOW_QUERIES=true
LOG_MEMORY_USAGE=true
LOG_AUTH_ATTEMPTS=true
LOG_API_CALLS=true
LOG_EXTERNAL_APIS=true
VERBOSE_LOGGING=false

# Development Features
ENABLE_DEVELOPMENT_FEATURES=false
ENABLE_TESTING_MODE=false
ENABLE_PROFILING=false
'''

    with open('env.example', 'w', encoding='utf-8') as f:
        f.write(example_content)
    print('✅ Created env.example file')

    # Clean up .env file by keeping only actual values (not placeholders)
    cleaned_content = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            cleaned_content.append(line)
        elif '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                key, value = parts
                key = key.strip()
                value = value.strip()
                if value and value not in ['your_discord_bot_token_here', 'your_twitch_token', 'your_channel', 'your_openai_key', 'change_this_in_production', 'admin123', 'dev_secret_change_in_production', 'prod_secret_change_in_production']:
                    cleaned_content.append(f'{key}={value}')
                else:
                    cleaned_content.append(f'# {key}=YOUR_{key.upper()}_HERE')
        elif line:
            cleaned_content.append(line)

    with open('.env', 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_content))
    print('✅ Cleaned up .env file (removed placeholders)')

if __name__ == '__main__':
    main()