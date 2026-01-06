# Website Manager MCP Server

MCP server for managing WordPress sites and website operations. Enables agents to create pages, deploy files, manage menus, create blog posts, and generate image prompts.

## Configuration

Add to your MCP settings (e.g., Claude Desktop config):

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

## Available Tools

### WordPress Management

#### 1. `create_wordpress_page`
Create a new WordPress page

**Parameters:**
- `site_key` (required): Site key (e.g., 'prismblossom', 'freerideinvestor')
- `page_name` (required): Page name/title
- `page_slug` (optional): Page slug (URL-friendly name)
- `template_name` (optional): Template name

**Example:**
```json
{
  "name": "create_wordpress_page",
  "arguments": {
    "site_key": "freerideinvestor",
    "page_name": "Trading Strategy Guide",
    "page_slug": "trading-strategy-guide"
  }
}
```

#### 2. `deploy_file_to_wordpress`
Deploy a file to WordPress site

**Parameters:**
- `site_key` (required): Site key
- `local_path` (required): Local file path
- `remote_path` (required): Remote file path on server
- `file_type` (optional): Type of file - "theme", "plugin", or "file" (default: "file")

**Example:**
```json
{
  "name": "deploy_file_to_wordpress",
  "arguments": {
    "site_key": "freerideinvestor",
    "local_path": "templates/page-template.php",
    "remote_path": "wp-content/themes/custom/page-template.php",
    "file_type": "theme"
  }
}
```

#### 3. `add_page_to_menu`
Add a page to WordPress menu

**Parameters:**
- `site_key` (required): Site key
- `page_slug` (required): Page slug to add to menu
- `menu_text` (optional): Menu text (defaults to page slug)

**Example:**
```json
{
  "name": "add_page_to_menu",
  "arguments": {
    "site_key": "freerideinvestor",
    "page_slug": "trading-strategy-guide",
    "menu_text": "Strategy Guide"
  }
}
```

#### 4. `list_wordpress_pages`
List all pages on WordPress site

**Parameters:**
- `site_key` (required): Site key

**Example:**
```json
{
  "name": "list_wordpress_pages",
  "arguments": {
    "site_key": "freerideinvestor"
  }
}
```

#### 5. `purge_wordpress_cache`
Purge WordPress cache

**Parameters:**
- `site_key` (required): Site key

**Example:**
```json
{
  "name": "purge_wordpress_cache",
  "arguments": {
    "site_key": "freerideinvestor"
  }
}
```

### Blog Automation

#### 6. `create_blog_post`
Create a blog post for a site

**Parameters:**
- `site_name` (required): Site name (e.g., 'freerideinvestor', 'tradingrobotplug.com')
- `strategy_name` (optional): Strategy name (e.g., 'tsla')

**Example:**
```json
{
  "name": "create_blog_post",
  "arguments": {
    "site_name": "freerideinvestor",
    "strategy_name": "tsla"
  }
}
```

#### 7. `create_report_page`
Create a report page for a site

**Parameters:**
- `site_name` (required): Site name
- `strategy_name` (optional): Strategy name
- `premium` (optional): Whether this is a premium report (default: false)

**Example:**
```json
{
  "name": "create_report_page",
  "arguments": {
    "site_name": "tradingrobotplug.com",
    "strategy_name": "tsla",
    "premium": true
  }
}
```

### Image Generation

#### 8. `generate_image_prompts`
Generate image prompts for website design

**Parameters:**
- `output_dir` (optional): Output directory for prompts

**Example:**
```json
{
  "name": "generate_image_prompts",
  "arguments": {
    "output_dir": "trading_robot/website_design/generated_images"
  }
}
```

## Integration with Agent Operating Cycle

### For Website Tasks

**CYCLE START:**
- Check if task involves website operations
- Review site requirements from DELEGATION_BOARD

**DURING CYCLE:**
- Use `create_wordpress_page` for new pages
- Use `deploy_file_to_wordpress` for file deployments
- Use `create_blog_post` for content creation

**CYCLE END:**
- Use `purge_wordpress_cache` after deployments
- Update MASTER_TASK_LOG with completion status

## Common Workflows

### Creating a New Page

1. Create page: `create_wordpress_page(site_key, page_name, page_slug)`
2. Add to menu: `add_page_to_menu(site_key, page_slug)`
3. Deploy template: `deploy_file_to_wordpress(site_key, local_path, remote_path, "theme")`
4. Purge cache: `purge_wordpress_cache(site_key)`

### Setting Up Brand Content

1. Create ICP definition: `create_icp_definition(site_key, icp_title, icp_content, target_demographic, pain_points, desired_outcomes)`
2. Create offer ladder: `create_offer_ladder(site_key, offer_title, offer_content, offer_tier, pricing)`
3. Verify content: Check `/wp-json/wp/v2/icp_definition` and `/wp-json/wp/v2/offer_ladder` endpoints

### Setting Up Sales Funnel

1. Create lead magnet page: `create_lead_magnet_page(site_key, page_title, magnet_content, magnet_type, download_url)`
2. Setup email integration: `setup_email_integration(site_key, service_provider, api_key, list_id)`
3. Setup payment integration: `setup_payment_integration(site_key, provider, publishable_key, secret_key)`
4. Create thank-you page: `create_wordpress_page(site_key, "Thank You", "thank-you")`

### Creating Blog Content

1. Generate blog post: `create_blog_post(site_name, strategy_name)`
2. Create report page: `create_report_page(site_name, strategy_name, premium)`
3. Update task log: Mark task complete in MASTER_TASK_LOG

### Brand Content Management

#### 8. `create_offer_ladder`
Create offer ladder content for a site

**Parameters:**
- `site_key` (required): Site key
- `offer_title` (required): Title of the offer
- `offer_content` (required): Content/description of the offer
- `offer_tier` (optional): Tier level - "free", "core", "premium", "enterprise" (default: "core")
- `pricing` (optional): Pricing information

**Example:**
```json
{
  "name": "create_offer_ladder",
  "arguments": {
    "site_key": "freerideinvestor",
    "offer_title": "Trading Strategy Mastery",
    "offer_content": "Master proven trading strategies with our comprehensive course and live signals.",
    "offer_tier": "premium",
    "pricing": "$497/month"
  }
}
```

#### 9. `create_icp_definition`
Create ICP (Ideal Customer Profile) definition for a site

**Parameters:**
- `site_key` (required): Site key
- `icp_title` (required): Title of the ICP definition
- `icp_content` (required): Content/description of the ICP
- `target_demographic` (optional): Target demographic for this ICP
- `pain_points` (optional): Pain points this ICP experiences
- `desired_outcomes` (optional): Desired outcomes this ICP wants

**Example:**
```json
{
  "name": "create_icp_definition",
  "arguments": {
    "site_key": "freerideinvestor",
    "icp_title": "FreeRide Investor Ideal Customer Profile",
    "icp_content": "For active traders struggling with inconsistent results, we eliminate guesswork and provide proven trading strategies.",
    "target_demographic": "Active traders (day/swing traders, $10K-$500K accounts)",
    "pain_points": "inconsistent results, guesswork",
    "desired_outcomes": "consistent edge, reduced losses, trading confidence"
  }
}
```

### Lead Generation & Sales Funnel

#### 10. `create_lead_magnet_page`
Create a lead magnet page with download/opt-in functionality

**Parameters:**
- `site_key` (required): Site key
- `page_title` (required): Title of the lead magnet page
- `magnet_content` (required): Content for the lead magnet page
- `magnet_type` (optional): Type - "ebook", "webinar", "checklist", "template", "course" (default: "ebook")
- `download_url` (optional): Download URL for the magnet

**Example:**
```json
{
  "name": "create_lead_magnet_page",
  "arguments": {
    "site_key": "freerideinvestor",
    "page_title": "Free Trading Signals Guide",
    "magnet_content": "Download our comprehensive guide to understanding and using trading signals effectively.",
    "magnet_type": "ebook",
    "download_url": "/downloads/trading-signals-guide.pdf"
  }
}
```

#### 11. `setup_email_integration`
Setup email integration for lead capture

**Parameters:**
- `site_key` (required): Site key
- `service_provider` (optional): Email provider - "mailchimp", "convertkit", "sendinblue", "activecampaign" (default: "mailchimp")
- `api_key` (optional): API key for the email service
- `list_id` (optional): List/audience ID for the email service

**Example:**
```json
{
  "name": "setup_email_integration",
  "arguments": {
    "site_key": "freerideinvestor",
    "service_provider": "mailchimp",
    "api_key": "your-mailchimp-api-key",
    "list_id": "your-list-id"
  }
}
```

#### 12. `setup_payment_integration`
Setup payment integration for checkout functionality

**Parameters:**
- `site_key` (required): Site key
- `provider` (optional): Payment provider - "stripe", "paypal", "woocommerce" (default: "stripe")
- `publishable_key` (optional): Publishable API key
- `secret_key` (optional): Secret API key

**Example:**
```json
{
  "name": "setup_payment_integration",
  "arguments": {
    "site_key": "freerideinvestor",
    "provider": "stripe",
    "publishable_key": "pk_live_...",
    "secret_key": "sk_live_..."
  }
}
```

### Website Design

1. Generate image prompts: `generate_image_prompts(output_dir)`
2. Use prompts with image generation tool
3. Deploy images: `deploy_file_to_wordpress(site_key, local_path, remote_path)`

## Site Keys Reference

Common site keys:
- `prismblossom` - Prism Blossom site
- `freerideinvestor` - FreeRide Investor site
- `crosbyultimateevents` - Crosby Ultimate Events
- `tradingrobotplug` - Trading Robot Plug
- `houston sipqueen` - Houston Sip Queen
- `weareswarm` - We Are Swarm sites

## Benefits

1. **Centralized Website Operations** - All WordPress operations in one place
2. **Agent Automation** - Agents can manage websites automatically
3. **Content Creation** - Automated blog post and report generation
4. **File Deployment** - Easy theme/plugin file deployment
5. **Cache Management** - Automatic cache purging after changes

## Related Documents

- `tools/wordpress_manager.py` - WordPress management tool source
- `tools/strategy_blog_automation.py` - Blog automation source
- `trading_robot/website_design/` - Website design assets
- `DELEGATION_BOARD.md` - Task ownership for website tasks
- `MASTER_TASK_LOG.md` - Task tracking

## Troubleshooting

### Connection Failed
- Check site credentials in `.deploy_credentials/`
- Verify site key is correct
- Check network connectivity

### File Not Found
- Verify local file path exists
- Check file permissions
- Ensure file is in correct format

### Blog Post Failed
- Check site configuration in `.deploy_credentials/blogging_api.json`
- Verify site name matches config
- Check WordPress API credentials

