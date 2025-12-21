# Websites Repository Sync Setup Guide

This guide explains how to set up automatic syncing from the main project to the websites repository.

## Overview

The sync system automatically pushes changes from the main project to the websites repository when:
- Changes are made to web-related files
- Changes are pushed to main/develop branches
- Manual trigger via GitHub Actions

## Setup Steps

### 1. Create GitHub Repository

First, create a new GitHub repository for your websites (e.g., `Dadudekc/websites`).

### 2. Initialize Websites Repository

Run the setup tool to configure the local websites repository:

```bash
python tools/setup_websites_repo.py --repo-url https://github.com/Dadudekc/websites.git
```

This will:
- Initialize git repository (if needed)
- Set up remote origin
- Create .gitignore file

### 3. Configure GitHub Secrets

Add the following secrets to your main repository's GitHub Settings:

- **WEBSITES_REPO**: The full repository name (e.g., `Dadudekc/websites`)
- **WEBSITES_REPO_TOKEN**: A GitHub Personal Access Token with `repo` permissions

To create a token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Copy token and add to Secrets

### 4. Test Sync

Test the sync tool with a dry run:

```bash
python tools/sync_websites_repo.py --all --dry-run
```

This will show what would be synced without making changes.

### 5. Manual Sync

To manually sync changes:

```bash
# Sync all configured files
python tools/sync_websites_repo.py --all --commit

# Sync specific files
python tools/sync_websites_repo.py --files "src/web/theme.js" "docs/websites/guide.md" --commit
```

## Sync Configuration

The sync tool is configured to sync the following:

- `src/web/` → `src/web/`
- `src/discord_commander/web/` → `src/discord_commander/web/`
- `docs/websites/` → `docs/`
- `docs/deployment/` → `docs/deployment/`
- `tools/website_*.py` → `tools/`
- `tools/deploy_*.py` → `tools/`
- `.env.example` → `.env.example`

## Automatic Sync via GitHub Actions

The `.github/workflows/sync-websites.yml` workflow automatically:
- Triggers on pushes to main/develop branches
- Only runs when web-related files change
- Syncs changes to websites repository
- Commits and pushes automatically

## Manual Workflow

1. Make changes to web files in main project
2. Commit changes: `git commit -m "Update web components"`
3. Push to main: `git push origin main`
4. GitHub Actions automatically syncs to websites repo

## Troubleshooting

### Sync Fails

Check:
- Websites repository exists and is accessible
- GitHub token has correct permissions
- File paths are correct
- No merge conflicts in websites repo

### Files Not Syncing

Verify:
- Files match sync configuration patterns
- Files are not in .gitignore
- Files exist in source location

### GitHub Actions Not Triggering

Check:
- Workflow file is in `.github/workflows/`
- Secrets are configured correctly
- Branch name matches workflow trigger

## Advanced Usage

### Custom Sync Configuration

Edit `tools/sync_websites_repo.py` to modify sync patterns:

```python
self.sync_config = {
    "src/web/": "src/web/",
    # Add your custom mappings
}
```

### Exclude Files

Add patterns to exclude:

```python
self.exclude_patterns = [
    "__pycache__",
    "*.pyc",
    # Add your exclusions
]
```

## Support

For issues or questions, check:
- GitHub Actions logs
- Sync tool output
- Websites repository status

