# WP-CLI MCP Server

## Overview

The WP-CLI MCP Server provides WordPress command-line interface operations through the Model Context Protocol (MCP). This enables AI agents to perform automated WordPress management tasks including plugin/theme management, database operations, and content management.

## Features

### Plugin Management
- Install plugins from wordpress.org
- Activate/deactivate plugins
- Update plugins
- List plugins with status filtering

### Theme Management
- Install themes from wordpress.org
- Activate themes
- Update themes

### Database Operations
- Export database to SQL files
- Import database from SQL files
- Search and replace operations

### Content Management
- Create posts and pages
- Update existing content
- Manage post status and types

### Core Operations
- Update WordPress core
- Check for available updates
- Get site information

## Installation

1. Ensure WP-CLI is installed on your system:
   ```bash
   curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
   chmod +x wp-cli.phar
   sudo mv wp-cli.phar /usr/local/bin/wp
   ```

2. Verify WP-CLI installation:
   ```bash
   wp --version
   ```

## Usage

### As a Standalone Server

```bash
# List available tools
python -m mcp_servers.wp_cli_server.main --list-tools

# Show server information
python -m mcp_servers.wp_cli_server.main --server-info

# Run interactive server (accepts JSON requests from stdin)
python -m mcp_servers.wp_cli_server.main
```

### Specifying WordPress Path

```bash
python -m mcp_servers.wp_cli_server.main --wordpress-path /path/to/wordpress
```

## MCP Tool Interface

The server exposes WordPress operations as MCP tools. Each tool accepts JSON parameters and returns structured results.

### Example Tool Calls

```json
// Install and activate a plugin
{
  "tool": "wp_cli_install_plugin",
  "parameters": {
    "plugin_slug": "wordpress-seo",
    "activate": true
  }
}

// Create a new post
{
  "tool": "wp_cli_create_post",
  "parameters": {
    "title": "Hello World",
    "content": "This is my first post!",
    "status": "publish"
  }
}

// Export database
{
  "tool": "wp_cli_db_export",
  "parameters": {
    "output_file": "/path/to/backup.sql"
  }
}
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `wp_cli_install_plugin` | Install WordPress plugin | plugin_slug, activate |
| `wp_cli_activate_plugin` | Activate plugin | plugin_slug |
| `wp_cli_deactivate_plugin` | Deactivate plugin | plugin_slug |
| `wp_cli_update_plugin` | Update plugin | plugin_slug |
| `wp_cli_list_plugins` | List plugins | status_filter |
| `wp_cli_install_theme` | Install WordPress theme | theme_slug, activate |
| `wp_cli_activate_theme` | Activate theme | theme_slug |
| `wp_cli_db_export` | Export database | output_file |
| `wp_cli_db_import` | Import database | input_file |
| `wp_cli_db_search_replace` | Search/replace in DB | old_value, new_value, table |
| `wp_cli_create_post` | Create post/page | title, content, post_type, status |
| `wp_cli_update_post` | Update post | post_id, title, content |
| `wp_cli_core_update` | Update WordPress core | - |
| `wp_cli_get_site_info` | Get site information | - |

## Response Format

All tools return structured JSON responses:

```json
{
  "tool": "tool_name",
  "result": {
    "success": true,
    "stdout": "Command output",
    "stderr": "",
    "returncode": 0
  },
  // Tool-specific fields
}
```

## Error Handling

The server provides comprehensive error handling:

- WP-CLI availability checks
- Command timeout protection (5 minutes)
- Structured error responses
- Detailed logging

## Security Considerations

- Commands are executed with the permissions of the running user
- Database operations should be used with caution
- Consider running in isolated environments for production use
- Validate all inputs before execution

## Integration

This MCP server can be integrated with AI agents and automation systems that support the Model Context Protocol, enabling seamless WordPress management through natural language interfaces.

## V2 Compliance

- Author: Agent-1 (Integration & Core Systems Specialist)
- Date: 2026-01-16
- Domain: web
- Follows V2 architecture principles and standards