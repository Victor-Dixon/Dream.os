# Website Manager MCP Integration

**Purpose:** How agents use website management tools via MCP

**Last Updated:** 2025-12-16

---

## Overview

The website management system is exposed via MCP, allowing agents to:
- Create and manage WordPress pages
- Deploy files to websites
- Create blog posts and reports
- Generate image prompts
- Manage WordPress menus and cache

---

## MCP Server: website_manager_server

### Location
`mcp_servers/website_manager_server.py`

### Configuration
Add to MCP settings:

```json
{
  "mcpServers": {
    "website-manager": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/website_manager_server.py"
      ]
    }
  }
}
```

### Available Tools

1. **WordPress Management:**
   - `create_wordpress_page` - Create new pages
   - `deploy_file_to_wordpress` - Deploy files
   - `add_page_to_menu` - Add pages to menus
   - `list_wordpress_pages` - List all pages
   - `purge_wordpress_cache` - Clear cache

2. **Blog Automation:**
   - `create_blog_post` - Create blog posts
   - `create_report_page` - Create report pages

3. **Image Generation:**
   - `generate_image_prompts` - Generate design prompts

---

## Agent Workflow Examples

### Example 1: Creating a New Page

**Task:** Create "Trading Guide" page for FreeRideInvestor

1. **Create Page:**
   ```json
   {
     "name": "create_wordpress_page",
     "arguments": {
       "site_key": "freerideinvestor",
       "page_name": "Trading Guide",
       "page_slug": "trading-guide"
     }
   }
   ```

2. **Add to Menu:**
   ```json
   {
     "name": "add_page_to_menu",
     "arguments": {
       "site_key": "freerideinvestor",
       "page_slug": "trading-guide",
       "menu_text": "Trading Guide"
     }
   }
   ```

3. **Deploy Template (if needed):**
   ```json
   {
     "name": "deploy_file_to_wordpress",
     "arguments": {
       "site_key": "freerideinvestor",
       "local_path": "templates/trading-guide-template.php",
       "remote_path": "wp-content/themes/custom/trading-guide-template.php",
       "file_type": "theme"
     }
   }
   ```

4. **Purge Cache:**
   ```json
   {
     "name": "purge_wordpress_cache",
     "arguments": {
       "site_key": "freerideinvestor"
     }
   }
   ```

### Example 2: Creating Blog Content

**Task:** Create TSLA strategy blog post

1. **Create Blog Post:**
   ```json
   {
     "name": "create_blog_post",
     "arguments": {
       "site_name": "freerideinvestor",
       "strategy_name": "tsla"
     }
   }
   ```

2. **Create Report Page:**
   ```json
   {
     "name": "create_report_page",
     "arguments": {
       "site_name": "tradingrobotplug.com",
       "strategy_name": "tsla",
       "premium": false
     }
   }
   ```

3. **Update Task Log:**
   - Mark task complete in MASTER_TASK_LOG

### Example 3: Website Design

**Task:** Generate image prompts for new site design

1. **Generate Prompts:**
   ```json
   {
     "name": "generate_image_prompts",
     "arguments": {
       "output_dir": "trading_robot/website_design/generated_images"
     }
   }
   ```

2. **Use Prompts:**
   - Use generated prompts with image generation tool
   - Deploy images to site

---

## Integration with Task Management

### Website Tasks in DELEGATION_BOARD

Website tasks are assigned to:
- **SWARM** - For repetitive operations (deployments, content creation)
- **VICTOR** - For strategic decisions (which pages, what content)

### Task Workflow

1. **Task Assigned** (in DELEGATION_BOARD)
2. **Agent Checks** MASTER_TASK_LOG for website tasks
3. **Agent Executes** using website_manager MCP tools
4. **Agent Updates** MASTER_TASK_LOG with completion

---

## Common Site Keys

- `prismblossom` - Prism Blossom
- `freerideinvestor` - FreeRide Investor
- `crosbyultimateevents` - Crosby Ultimate Events
- `tradingrobotplug` - Trading Robot Plug
- `houston sipqueen` - Houston Sip Queen
- `weareswarm` - We Are Swarm

---

## Benefits

1. **Automated Website Management** - Agents can manage sites without manual intervention
2. **Content Creation** - Automated blog posts and reports
3. **File Deployment** - Easy theme/plugin updates
4. **Cache Management** - Automatic cache clearing
5. **Centralized Operations** - All website tools in one MCP server

---

## Related Documents

- `mcp_servers/WEBSITE_MANAGER_README.md` - Full tool documentation
- `tools/wordpress_manager.py` - WordPress tool source
- `tools/strategy_blog_automation.py` - Blog automation source
- `DELEGATION_BOARD.md` - Task assignments
- `MASTER_TASK_LOG.md` - Task tracking

