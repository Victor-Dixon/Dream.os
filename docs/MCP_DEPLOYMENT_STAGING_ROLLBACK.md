# Deployment Staging & Rollback Infrastructure

**Author:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-12-28  
**Status:** ✅ Implemented  
**V2 Compliant:** Yes

## Overview

The deployment MCP server has been enhanced with comprehensive staging and rollback capabilities, enabling safe WordPress deployments with instant rollback to any previous state.

## Implementation Details

### Core Components

1. **DeploymentSnapshot Data Structure** (`mcp_servers/deployment_server.py`)
   - Stores snapshot metadata, file lists, and backup paths
   - Serializable to JSON for persistence
   - Includes WordPress version, theme version, and deployment metadata

2. **SimpleWordPressDeployer Enhancements** (`websites/ops/deployment/simple_wordpress_deployer.py`)
   - Added `download_file()` method for file backup
   - Added `list_files()` method for directory listing
   - Added `file_exists()` method for file validation
   - Improved path handling for cross-platform compatibility

3. **Snapshot Management Functions**
   - `create_deployment_snapshot()` - Creates pre/post deployment snapshots
   - `list_deployment_snapshots()` - Lists available snapshots with filtering
   - `rollback_deployment()` - Restores site to previous snapshot state
   - `delete_deployment_snapshot()` - Removes old snapshots for storage management
   - `deploy_with_staging()` - Automatic staging deployment with rollback protection

## Architecture

### Snapshot Creation Flow

```
1. Connect to WordPress site via SimpleWordPressDeployer
2. Identify files to backup (theme files, plugin files, config files)
3. Download files to local backup directory
4. Generate snapshot metadata (WP version, theme version, file hashes)
5. Store snapshot JSON with backup paths
6. Return snapshot ID for rollback reference
```

### Rollback Flow

```
1. Load snapshot metadata from JSON file
2. Validate snapshot exists and belongs to site_key
3. Connect to WordPress site
4. Restore files from backup_paths to original locations
5. Verify restoration success
6. Return rollback results with restored/failed file counts
```

### Deployment with Staging Flow

```
1. Create pre-deployment snapshot
   └─> Backup current state
   └─> Store snapshot ID

2. Execute deployment
   └─> Deploy new files via SFTP
   └─> Verify deployment success

3. Create post-deployment snapshot
   └─> Backup new state
   └─> Store snapshot ID

4. Return comprehensive result
   └─> Deployment status
   └─> Pre/post snapshot IDs
   └─> Rollback availability
```

## File Structure

### Snapshot Storage

```
deployment_snapshots/
├── {site_key}/
│   ├── {snapshot_id}.json          # Snapshot metadata
│   └── {snapshot_id}/              # Backup files directory
│       ├── wp-content/themes/...
│       └── wp-content/plugins/...
```

### Snapshot JSON Format

```json
{
  "snapshot_id": "tradingrobotplug.com_20251228_120000_abc123def",
  "site_key": "tradingrobotplug.com",
  "timestamp": "2025-12-28T12:00:00.000000",
  "files": [
    {
      "path": "wp-content/themes/tradingrobotplug-theme/style.css",
      "backed_up": true,
      "backup_path": "deployment_snapshots/tradingrobotplug.com/abc123def/wp-content/themes/tradingrobotplug-theme/style.css"
    }
  ],
  "metadata": {
    "description": "Pre-deployment snapshot for TradingRobotPlug Phase 1",
    "wordpress_version": "6.4.2",
    "theme_version": "1.0.0",
    "plugin_count": 5,
    "created_by": "deployment_mcp_server"
  },
  "backup_paths": [
    "deployment_snapshots/tradingrobotplug.com/abc123def/wp-content/themes/tradingrobotplug-theme/style.css"
  ]
}
```

## Usage Examples

### Create Snapshot

```python
from mcp_servers.deployment_server import create_deployment_snapshot

result = create_deployment_snapshot(
    site_key="tradingrobotplug.com",
    description="Pre-deployment snapshot before theme update"
)

if result["success"]:
    snapshot_id = result["snapshot_id"]
    print(f"Snapshot created: {snapshot_id}")
```

### Deploy with Staging

```python
from mcp_servers.deployment_server import deploy_with_staging

result = deploy_with_staging(
    site_key="tradingrobotplug.com",
    theme_files=["style.css", "functions.php", "index.php"],
    description="Theme update with rollback capability"
)

if result["success"]:
    print(f"Deployment successful")
    print(f"Rollback available: {result['rollback_available']}")
    print(f"Rollback snapshot ID: {result['rollback_snapshot_id']}")
else:
    print(f"Deployment failed: {result.get('error')}")
```

### Rollback Deployment

```python
from mcp_servers.deployment_server import rollback_deployment

result = rollback_deployment(
    site_key="tradingrobotplug.com",
    snapshot_id="tradingrobotplug.com_20251228_120000_abc123def"
)

if result["success"]:
    rollback_info = result["rollback"]
    print(f"Rollback successful")
    print(f"Files restored: {rollback_info['files_to_restore']}")
    print(f"Restored: {len(rollback_info['restored_files'])}")
    print(f"Failed: {len(rollback_info['failed_restores'])}")
```

### List Snapshots

```python
from mcp_servers.deployment_server import list_deployment_snapshots

# List all snapshots
all_snapshots = list_deployment_snapshots()

# List snapshots for specific site
site_snapshots = list_deployment_snapshots(site_key="tradingrobotplug.com")

for snapshot in site_snapshots["snapshots"]:
    print(f"{snapshot['snapshot_id']} - {snapshot['timestamp']}")
    print(f"  Description: {snapshot['metadata']['description']}")
```

## Integration Points

### MCP Server Integration

The staging/rollback functions are exposed via the deployment MCP server:

```json
{
  "tools": {
    "create_deployment_snapshot": {
      "description": "Create a snapshot of current deployment state",
      "inputSchema": {
        "type": "object",
        "properties": {
          "site_key": {"type": "string"},
          "description": {"type": "string"}
        },
        "required": ["site_key"]
      }
    },
    "rollback_deployment": {
      "description": "Rollback deployment to a previous snapshot",
      "inputSchema": {
        "type": "object",
        "properties": {
          "site_key": {"type": "string"},
          "snapshot_id": {"type": "string"}
        },
        "required": ["site_key", "snapshot_id"]
      }
    }
  }
}
```

### WordPress Manager Integration

- Uses `SimpleWordPressDeployer` for SFTP operations
- Leverages `load_site_configs()` for credential management
- Integrates with existing deployment infrastructure

## Error Handling

### Snapshot Creation Errors

- **Connection failures**: Returns error with diagnostic information
- **File backup failures**: Logs warnings but continues with metadata-only snapshot
- **Permission errors**: Returns detailed error message with resolution steps

### Rollback Errors

- **Snapshot not found**: Returns clear error with available snapshots
- **File restoration failures**: Tracks failed restores separately from successful ones
- **Connection errors**: Returns error with retry recommendations

## Storage Management

### Retention Policy

- **Default**: Keep last 10 snapshots per site
- **Manual cleanup**: Use `delete_deployment_snapshot()` to remove old snapshots
- **Automatic cleanup**: (Future) Configurable retention period (default: 30 days)

### Storage Optimization

- Backup files stored in snapshot-specific directories
- Snapshot metadata stored separately from backup files
- Backup files can be compressed (future enhancement)

## Testing

### Test Suite

Run the staging/rollback test suite:

```bash
python tools/test_deployment_staging.py
```

### Test Coverage

- ✅ Snapshot creation
- ✅ Snapshot listing
- ✅ Snapshot deletion
- ✅ Staging deployment
- ✅ Rollback functionality
- ✅ Error handling

## Future Enhancements

1. **Automatic Cleanup**: Configurable retention policies
2. **Compression**: Compress backup files to save storage
3. **Database Snapshots**: Include WordPress database backups
4. **Incremental Snapshots**: Only backup changed files
5. **Snapshot Verification**: Hash verification for file integrity
6. **Rollback Preview**: Show what will be restored before rollback
7. **Multi-Site Support**: Snapshot management for WordPress multisite

## Status

- ✅ Snapshot creation implemented
- ✅ Rollback functionality implemented
- ✅ Staging deployment implemented
- ✅ Documentation created
- ⏳ Production testing pending
- ⏳ Performance optimization pending

## References

- `mcp_servers/deployment_server.py` - Main implementation
- `websites/ops/deployment/simple_wordpress_deployer.py` - SFTP operations
- `tools/test_deployment_staging.py` - Test suite
- `docs/MCP_CONSOLIDATION_IMPLEMENTATION.md` - Overall MCP architecture

