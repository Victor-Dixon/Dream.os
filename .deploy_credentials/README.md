# Deployment Credentials

This directory contains deployment credentials for websites and services.

## ⚠️ SECURITY WARNING

**NEVER commit actual credential files to git!**

The following files contain sensitive information and are excluded from git:
- `sites.json` - SFTP/FTP credentials
- `blogging_api.json` - WordPress REST API credentials

## Example Files

The following example files are safe to commit and serve as templates:
- `sites.example.json` - Template for SFTP/FTP credentials
- `blogging_api.example.json` - Template for WordPress REST API credentials

## Setup Instructions

1. **Copy example files:**
   ```bash
   cp .deploy_credentials/sites.example.json .deploy_credentials/sites.json
   cp .deploy_credentials/blogging_api.example.json .deploy_credentials/blogging_api.json
   ```

2. **Fill in your actual credentials:**
   - Edit `sites.json` with your SFTP/FTP connection details
   - Edit `blogging_api.json` with your WordPress REST API credentials

3. **Sync to website configs (optional):**
   If you want to sync these credentials to the websites configs:
   ```bash
   cd D:\websites
   python tools/sync_site_credentials.py
   ```

## File Structure

### `sites.json`
Contains SFTP/FTP deployment credentials:
- `host` - Server IP or hostname
- `username` - SFTP username
- `password` - SFTP password
- `port` - SFTP port (typically 65002)
- `remote_path` - Remote directory path
- `site_url` - Website URL

### `blogging_api.json`
Contains WordPress REST API credentials:
- `username` - WordPress username
- `app_password` - WordPress application password
- `site_url` - Website URL
- `purpose` - Site purpose/category
- `categories` - Default post categories
- `default_tags` - Default post tags

## Security Best Practices

- Never commit actual credential files
- Use strong, unique passwords
- Rotate credentials regularly
- Limit access to this directory
- Use environment variables for CI/CD pipelines
- Consider using a password manager for credential storage

