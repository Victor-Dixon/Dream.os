# Git Push Credential Fix Guide

## Issue
403 Permission denied when pushing to `https://github.com/Victor-Dixon/Dream.os.git`

## Root Cause
Git credentials are cached for wrong account (Dadudekc instead of Victor-Dixon)

## Solutions

### Option 1: Update Credential Helper (Recommended)
```bash
# Clear cached credentials
git credential-manager-core erase
# Or on Windows:
git credential-manager erase https://github.com

# When prompted, use Victor-Dixon credentials
git push origin main
```

### Option 2: Use Personal Access Token
```bash
# Push with token in URL (one-time)
git push https://<TOKEN>@github.com/Victor-Dixon/Dream.os.git main

# Or configure credential helper to use token
git config credential.helper store
# Then push (will prompt for token)
git push origin main
```

### Option 3: Use SSH (If Configured)
```bash
# Change remote to SSH
git remote set-url origin git@github.com:Victor-Dixon/Dream.os.git
git push origin main
```

### Option 4: Manual Credential Update
1. Open Windows Credential Manager
2. Search for "github.com"
3. Remove/update credentials for github.com
4. Try push again (will prompt for new credentials)

## Verification
```bash
# Check remote URL
git remote -v

# Test connection
git ls-remote origin

# Check current user
git config user.name
git config user.email
```

