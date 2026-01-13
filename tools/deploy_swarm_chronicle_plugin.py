#!/usr/bin/env python3
"""
Deploy Swarm Chronicle Plugin to weareswarm.site
===============================================

Deploys the Swarm Chronicle WordPress plugin to display the complete Swarm operating chronicle.

Usage:
    python tools/deploy_swarm_chronicle_plugin.py [--dry-run]

Author: Agent-2 (Deployment Specialist)
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from mcp_servers.deployment_server import deploy_wordpress_file
except ImportError:
    # Try alternative import path
    try:
        import sys
        sys.path.append('mcp_servers')
        from deployment_server import deploy_wordpress_file
    except ImportError:
        print("❌ Cannot import deployment server")
        sys.exit(1)


def deploy_plugin_files(site_key: str = "weareswarm.online") -> bool:
    """Deploy all plugin files to WordPress site."""

    plugin_local_path = project_root / "sites" / "weareswarm.site" / "wp-content" / "plugins" / "swarm-chronicle-plugin"
    remote_base_path = "wp-content/plugins/swarm-chronicle-plugin"

    if not plugin_local_path.exists():
        print(f"❌ Plugin directory not found: {plugin_local_path}")
        return False

    print(f"🚀 Deploying Swarm Chronicle Plugin to {site_key}")

    # Get all plugin files
    plugin_files = []
    for root, dirs, files in os.walk(plugin_local_path):
        for file in files:
            if file.startswith('.') or file.endswith('.pyc'):
                continue

            local_file_path = Path(root) / file
            relative_path = local_file_path.relative_to(plugin_local_path)
            remote_path = f"{remote_base_path}/{relative_path}"

            plugin_files.append((local_file_path, remote_path))

    print(f"📦 Found {len(plugin_files)} files to deploy")

    # Deploy each file
    success_count = 0
    for local_path, remote_path in plugin_files:
        print(f"  📄 {remote_path}")
        result = deploy_wordpress_file(
            site_key=site_key,
            local_path=str(local_path),
            remote_path=remote_path,
            file_type="plugin"
        )

        if result.get('success'):
            success_count += 1
        else:
            print(f"    ❌ Failed: {result.get('error', 'Unknown error')}")

    print(f"\n✅ Successfully deployed {success_count}/{len(plugin_files)} files")

    if success_count == len(plugin_files):
        print("\n🎉 Swarm Chronicle Plugin deployment completed!")
        print("📝 Next steps:")
        print("   1. Go to WordPress admin → Plugins")
        print("   2. Activate 'Swarm Chronicle' plugin")
        print("   3. Configure API settings in plugin settings")
        print("   4. Add shortcodes to pages: [swarm_chronicle], [swarm_missions], etc.")
        return True

    return False


def create_plugin_readme():
    """Create a README for the plugin."""
    readme_content = """# Swarm Chronicle WordPress Plugin

Displays the complete Swarm operating chronicle including cycle accomplishments, project state, and mission logs.

## Features

- **Complete Chronicle Display**: Shows all Swarm activities, accomplishments, and missions
- **Real-time Synchronization**: Syncs data from Swarm systems via API
- **Multiple Views**: Different shortcodes for missions, accomplishments, and project state
- **Admin Dashboard**: WordPress admin interface for configuration and monitoring
- **REST API**: Programmatic access to chronicle data

## Shortcodes

### [swarm_chronicle]
Display the main chronicle overview
```
[swarm_chronicle type="overview" limit="50" agent="all"]
```

### [swarm_missions]
Show active missions and tasks
```
[swarm_missions status="active" limit="20" agent="Agent-1"]
```

### [swarm_accomplishments]
Display recent accomplishments
```
[swarm_accomplishments period="current" limit="25" agent="all"]
```

### [swarm_project_state]
Show project metrics and health
```
[swarm_project_state detail="summary" metrics="true"]
```

## Installation

1. Upload plugin files to `wp-content/plugins/swarm-chronicle-plugin/`
2. Activate the plugin in WordPress admin
3. Configure API settings in Settings → Swarm Chronicle
4. Add shortcodes to your pages/posts

## Configuration

### API Settings
- **API Endpoint**: URL of the Swarm API server
- **API Key**: Authentication key for API access
- **Auto Sync**: Enable automatic data synchronization
- **Sync Interval**: How often to sync data (hourly, daily, etc.)

### Manual Sync
Use the "Sync Now" button in the admin dashboard to manually trigger data synchronization.

## Data Sources

The plugin syncs data from multiple Swarm systems:

- **Master Task Log**: All missions, tasks, and objectives
- **Cycle Accomplishments**: Weekly/monthly achievement reports
- **Project Scanner**: Codebase analysis and metrics
- **Agent Activity**: Individual agent contributions and status

## API Endpoints

### GET /wp-json/swarm-chronicle/v1/data
Retrieve chronicle data
```
GET /wp-json/swarm-chronicle/v1/data?type=missions&limit=20&agent=Agent-1
```

### POST /wp-json/swarm-chronicle/v1/sync
Sync data from external sources (admin only)
```
POST /wp-json/swarm-chronicle/v1/sync
Authorization: Bearer {api_key}
```

## Development

### File Structure
```
swarm-chronicle-plugin/
├── swarm-chronicle-plugin.php      # Main plugin file
├── includes/
│   ├── class-swarm-chronicle.php   # Main plugin class
│   ├── class-chronicle-api.php     # API and data handling
│   └── class-chronicle-admin.php   # Admin interface
├── assets/
│   ├── css/
│   │   └── swarm-chronicle.css     # Frontend styles
│   └── js/
│       └── swarm-chronicle.js      # Frontend scripts
└── README.md                       # This file
```

### Hooks and Filters

#### Actions
- `swarm_chronicle_data_synced` - Fired after successful data sync
- `swarm_chronicle_api_error` - Fired on API errors

#### Filters
- `swarm_chronicle_api_endpoint` - Modify API endpoint URL
- `swarm_chronicle_display_limit` - Modify default display limits
- `swarm_chronicle_allowed_agents` - Filter allowed agents

## Support

For issues and feature requests, please contact the Swarm development team.

## License

MIT License - see LICENSE file for details.
"""

    readme_path = project_root / "sites" / "weareswarm.site" / "wp-content" / "plugins" / "swarm-chronicle-plugin" / "README.md"

    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ Created plugin README.md")
    except Exception as e:
        print(f"❌ Failed to create README: {e}")


def main():
    """Main deployment function."""
    import argparse

    parser = argparse.ArgumentParser(description='Deploy Swarm Chronicle Plugin to weareswarm.site')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deployed without actually deploying')
    parser.add_argument('--site-key', default='weareswarm.online', help='Target site key')

    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be deployed")
        print("📦 Plugin would be deployed to:", args.site_key)
        return

    print("🤖 SWARM CHRONICLE PLUGIN DEPLOYMENT")
    print("=" * 50)

    # Create README
    create_plugin_readme()

    # Deploy plugin files
    if deploy_plugin_files(args.site_key):
        print("\n🎯 DEPLOYMENT COMPLETE!")
        print(f"   Target Site: {args.site_key}")
        print("   Plugin: swarm-chronicle-plugin")
        print("   Status: Ready for activation")
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()