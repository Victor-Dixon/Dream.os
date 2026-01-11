# PowerShell script to set all environment variables from .env file
# Run this script to set all environment variables in your PowerShell session

Write-Host "🔧 Setting environment variables..." -ForegroundColor Green

# Discord Bot Configuration
$env:DISCORD_BOT_TOKEN = "***REMOVED***"
$env:DISCORD_GUILD_ID = "1375298054357254257"

# Docker Configuration
$env:COMPOSE_PROJECT_NAME = "dream-os"

# Environment Settings
$env:ENVIRONMENT = "development"
$env:LOG_LEVEL = "INFO"
$env:DEBUG_MODE = "false"

# Web Server Settings
$env:WEB_HOST = "127.0.0.1"
$env:WEB_PORT = "5000"
$env:WEB_WORKERS = "4"

# API Settings
$env:API_TIMEOUT = "30"
$env:API_RATE_LIMIT = "100"

# Database Settings
$env:DB_CONNECTION_TIMEOUT = "10"
$env:DB_POOL_SIZE = "10"

# File Paths
$env:LOG_DIRECTORY = "logs"
$env:CONFIG_DIRECTORY = "config"
$env:DATA_DIRECTORY = "data"
$env:CACHE_DIRECTORY = "cache"

# Performance Settings
$env:SLOW_QUERY_THRESHOLD = "1.0"
$env:MEMORY_THRESHOLD = "100"

# Agent System Configuration
$env:AGENT_COUNT = "8"
$env:CAPTAIN_ID = "Agent-4"
$env:DEFAULT_MODE = "pyautogui"

# Browser Automation
$env:GPT_URL = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
$env:MAX_SCRAPE_RETRIES = "3"

# Test Configuration
$env:COVERAGE_THRESHOLD = "80.0"
$env:TEST_FAILURE_THRESHOLD = "0"

# Advanced Timeouts
$env:SCRAPE_TIMEOUT = "30.0"
$env:RESPONSE_WAIT_TIMEOUT = "120.0"
$env:SMOKE_TEST_TIMEOUT = "60"
$env:UNIT_TEST_TIMEOUT = "120"
$env:INTEGRATION_TEST_TIMEOUT = "300"

# File Patterns
$env:ARCHITECTURE_FILES = "\.(py|js|ts|java|cpp|h|md)$"
$env:TEST_FILES = "(test|spec)\.(py|js|ts|java)$"

# Performance Targets
$env:RESPONSE_TIME_TARGET = "100.0"
$env:THROUGHPUT_TARGET = "1000.0"
$env:LATENCY_TARGET = "50.0"

# Advanced Logging
$env:LOG_SLOW_QUERIES = "true"
$env:LOG_MEMORY_USAGE = "true"
$env:LOG_AUTH_ATTEMPTS = "true"
$env:LOG_API_CALLS = "true"
$env:LOG_EXTERNAL_APIS = "true"
$env:VERBOSE_LOGGING = "true"

# Development Features
$env:ENABLE_DEVELOPMENT_FEATURES = "true"
$env:ENABLE_TESTING_MODE = "false"
$env:ENABLE_PROFILING = "false"

# Website Configuration
$env:SWARM_WEBSITE_URL = "https://tradingrobotplug.com"
$env:SWARM_WEBSITE_USERNAME = "dadudekc@gmail.com"
$env:SWARM_WEBSITE_PASSWORD = "Falcons#1247"

# Logging Configuration
$env:LOG_FILE = "logs/app.log"

# Hostinger Configuration
$env:HOSTINGER_HOST = "157.173.214.121"
$env:HOSTINGER_USER = "u996867598"
$env:HOSTINGER_PASS = "Falcons#1247"
$env:HOSTINGER_PORT = "65002"
$env:HOSTINGER_API_KEY = "xxOVtoufulp3BCN3wj73kWNnGCqhXoGNVtyVRiG7448147b3"

# Discord Bot Settings
$env:DISCORD_COMMAND_PREFIX = "!"
$env:DISCORD_BOT_STATUS = '"🐝 WE ARE SWARM - Agent Coordination Active"'
$env:DISCORD_BOT_ACTIVITY_TYPE = "watching"
$env:DISCORD_COMMANDER_LOG_LEVEL = "INFO"
$env:DISCORD_COMMANDER_AUTO_START = "true"
$env:DISCORD_COMMANDER_HEALTH_CHECK_INTERVAL = "30"

# Discord Channel IDs
$env:MAJOR_UPDATE_DISCORD_CHANNEL_ID = "1387221819966230528"
$env:MMORPG_CHANNEL = "1387221305211752580"
$env:MMORPG_STORY_CHANNEL = "1387516270269829250"
$env:MMORPG_LORE_CHANNEL = "1387516323168391239"
$env:MMORPG_EQUIPMENT_CHANNEL = "1387516402847711364"
$env:MMORPG_QUESTS_CHANNEL = "1387516494287732999"
$env:MMORPG_SKILLS_CHANNEL = "1387516565632585729"
$env:DISCORD_CHANNEL_ID = "1387221819966230528"

# Agent-specific Discord Channels
$env:DISCORD_CHANNEL_AGENT_1 = "1387514611351421079"
$env:DISCORD_CHANNEL_AGENT_2 = "1387514933041696900"
$env:DISCORD_CHANNEL_AGENT_3 = "1387515009621430392"
$env:DISCORD_CHANNEL_AGENT_4 = "1387514978348826664"
$env:DISCORD_CHANNEL_AGENT_5 = "1415916580910665758"
$env:DISCORD_CHANNEL_AGENT_6 = "1415916621847072828"
$env:DISCORD_CHANNEL_AGENT_7 = "1415916665283022980"
$env:DISCORD_CHANNEL_AGENT_8 = "1415916707704213565"

# Discord Webhooks
$env:DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1404867570510725120/***REMOVED***"
$env:DISCORD_WEBHOOK_AGENT_1 = "https://discordapp.com/api/webhooks/1423941506850492416/***REMOVED***"
$env:DISCORD_WEBHOOK_AGENT_2 = "https://discordapp.com/api/webhooks/1423941931423240243/***REMOVED***"
$env:DISCORD_WEBHOOK_AGENT_3 = "https://discordapp.com/api/webhooks/1423942060876238900/3ZZdLIVyWXLGbMJBDlV8eO3gqCXaKymeLepKmfUCW0o9XzfMdyGTrA7U_ybg3TvVSkmh"
$env:DISCORD_WEBHOOK_AGENT_4 = "https://discordapp.com/api/webhooks/1423942177381421186/***REMOVED***"
$env:DISCORD_WEBHOOK_AGENT_5 = "https://discordapp.com/api/webhooks/1423942323024171068/***REMOVED***"
$env:DISCORD_WEBHOOK_AGENT_6 = "https://discordapp.com/api/webhooks/1423942441815375922/LEWnwF3BkeMyTbaoznlRVCasgMWukEwl9zDC-CkT1Jltms0JxMfwteJ4qonsrGMOx2ek"
$env:DISCORD_WEBHOOK_AGENT_7 = "https://discordapp.com/api/webhooks/1423942538536157305/7M5tIEsXLChfFi9UMg35UmA2oMcAee_gOqqQB5JtGnUeF8rWlcoBohMykPeI5-uxfVlN"
$env:DISCORD_WEBHOOK_AGENT_8 = "https://discordapp.com/api/webhooks/1423942673940611072/D1o0bEdKYUaONrnHSuCoFdprRYC2I2SX2t_dhJEVtdNACOTqssH8vdO2b9oEJhykP0oT"

# Flask Configuration
$env:FLASK_DEBUG = "false"
$env:LOG_FILE_ACCESS = "false"
$env:MASK_SENSITIVE_DATA = "true"
$env:LOG_DATABASE_CONNECTIONS = "true"
$env:LOG_MESSAGE_QUEUE = "true"
$env:LOG_WEBSOCKET = "true"

# API Configuration
$env:API_RETRY_ATTEMPTS = "3"
$env:DB_QUERY_TIMEOUT = "30"
$env:WEB_TIMEOUT = "60"

# Quality and Metrics
$env:QUALITY_CHECK_INTERVAL = "30.0"
$env:METRICS_COLLECTION_INTERVAL = "60.0"

# Test Timeouts
$env:PERFORMANCE_TEST_TIMEOUT = "600"
$env:SECURITY_TEST_TIMEOUT = "180"
$env:API_TEST_TIMEOUT = "240"
$env:COORDINATION_TEST_TIMEOUT = "180"
$env:LEARNING_TEST_TIMEOUT = "180"

# Coordination and Testing
$env:COORDINATE_MODE = "8-agent"
$env:TEST_FILE_PATTERN = "test_*.py"

# File Patterns
$env:CONFIG_FILES = "(config|settings|env|yml|yaml|json|toml|ini)$"
$env:DOCS_FILES = "(README|CHANGELOG|CONTRIBUTING|docs?)\.md$"
$env:BUILD_FILES = "(Dockerfile|docker-compose|\.gitlab-ci|\.github|Makefile|build\.gradle|pom\.xml)$"

# Performance Targets
$env:PERFORMANCE_DEGRADATION_THRESHOLD = "100.0"
$env:SCALABILITY_TARGET = "100"
$env:RELIABILITY_TARGET = "99.9"

# Messaging Timeouts
$env:SINGLE_MESSAGE_TIMEOUT = "1.0"
$env:BULK_MESSAGE_TIMEOUT = "10.0"
$env:CONCURRENT_MESSAGE_TIMEOUT = "5.0"
$env:MIN_THROUGHPUT = "10.0"
$env:MAX_MEMORY_PER_MESSAGE = "1024"

# ChatGPT Integration
$env:CONVERSATION_URL = "https://chatgpt.com/c/68bf1b1b-37b8-8324-be55-e3ccf20af737"
$env:INPUT_SELECTOR = "textarea[data-testid='prompt-textarea']"
$env:SEND_BUTTON_SELECTOR = "button[data-testid='send-button']"
$env:RESPONSE_SELECTOR = "[data-testid='conversation-turn']:last-child .markdown"
$env:THINKING_INDICATOR = "[data-testid='thinking-indicator']"

# Reporting Configuration
$env:COVERAGE_REPORT_PRECISION = "2"
$env:HISTORY_WINDOW = "100"
$env:REPORTS_DIR = "reports"
$env:INCLUDE_METADATA = "true"
$env:INCLUDE_RECOMMENDATIONS = "true"

# Application Settings
$env:DEFAULT_MAX_WORKERS = "4"
$env:APP_ENV = "development"

# Debug Settings
$env:MESSAGING_DEBUG = "true"
$env:SCANNER_VERBOSE = "true"
$env:DEBATE_DEBUG = "true"
$env:ONBOARDING_VERBOSE = "true"
$env:PERFORMANCE_DEBUG = "true"

# External Services
$env:PROMETHEUS_URL = "http://localhost:9090"
$env:POSTGRES_CONNECTION_STRING = "postgresql://user:password@localhost:5432/agent_cellphone"

# API Keys (Financial Data)
$env:ALPHAVANTAGE_API_KEY = "C6AG9NZX6QIPYTX4"
$env:POLYGONIO_API_KEY = "ruqNOBWgLAXuiUM0ugL5WmxbkIdlELp4"
$env:NASDAQ_API_KEY = "5hSXmst5GSPX2F2VauxN"
$env:FINNHUB_API_KEY = "ckuqs6pr01qmtr8lh750ckuqs6pr01qmtr8lh75g"
$env:FRED_API_KEY = "7e597dfc16d17cf4cac13ce7901de50d"
$env:GEMINI_API_KEY = "AIzaSyDSQmPecOnB4nhBREv6r7WPer8rTLRCtkQ"
$env:GITHUB_TOKEN = "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"

# Account Credentials
$env:ROBINHOOD_USERNAME = "DaDudeKC@gmail.com"
$env:GUM_USER = "DaDudeKC@gmail.com"
$env:GUM_PASS = "Falcons#1247"
$env:ROBINHOOD_PASSWORD = "Falcons#1247"

# GitHub Tokens
$env:FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN = "***REMOVED***"
$env:GH_TOKEN = "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"

# Twitch Configuration
$env:TWITCH_ACCESS_TOKEN = "f3wjto5gdvd41m3izza7j8wbtlqsgr"
$env:TWITCH_USERNAME = "weareswarm"
$env:TWITCH_CHANNEL = "https://www.twitch.tv/digital_dreamscape"

Write-Host "All environment variables set successfully!" -ForegroundColor Green
Write-Host "Discord bot token is configured and ready to use." -ForegroundColor Cyan