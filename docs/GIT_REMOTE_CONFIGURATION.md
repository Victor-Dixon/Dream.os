<<<<<<< HEAD
<<<<<<< HEAD
<!-- SSOT Domain: documentation -->

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
<!-- SSOT Domain: documentation -->

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
# Git Remote Configuration

**Date**: 2025-12-22  
**Status**: ✅ Configured

## Remote Configuration

The repository is configured with multiple remotes for flexibility and backup:

### Primary Remote (Dream.os)
- **Name**: `origin`
- **URL**: `https://github.com/Victor-Dixon/Dream.os.git`
- **Purpose**: Primary repository (Dream.os)
- **Default**: Used by `git push` and `git pull` without specifying remote

### Backup Remote (Old Repository)
- **Name**: `old-origin`
- **URL**: `https://github.com/Dadudekc/Agent_Cellphone_V2_Repository.git`
- **Purpose**: Backup/mirror of old repository
- **Usage**: Explicit remote name required

### Additional Remotes
- **`dream-os`**: `https://github.com/Victor-Dixon/Dream.os.git` (with token, if needed)
- **`cleaned-mirror`**: Local path (local backup)

---

## Usage Examples

### Pushing to Remotes

```bash
# Push to Dream.os (primary - default)
git push origin main

# Push to old repository (backup)
git push old-origin main

# Push to both repositories
git push origin main
git push old-origin main
```

### Pulling from Remotes

```bash
# Pull from Dream.os (primary)
git pull origin main

# Pull from old repository (backup)
git pull old-origin main

# Fetch from both
git fetch origin
git fetch old-origin
```

### Viewing Remote Information

```bash
# List all remotes
git remote -v

# Show remote details
git remote show origin
git remote show old-origin
```

### Default Behavior

- **`git push`** (without remote): Pushes to `origin` (Dream.os)
- **`git pull`** (without remote): Pulls from `origin` (Dream.os)
- **Explicit remote required**: Use `old-origin` explicitly to access old repository

---

## Workflow Recommendations

### Daily Workflow
1. Work on `main` branch locally
2. Push to `origin` (Dream.os) as primary
3. Optionally push to `old-origin` for backup

### Backup Strategy
- **Primary**: `origin` (Dream.os) - main repository
- **Backup**: `old-origin` - old repository (mirror)
- **Local**: `cleaned-mirror` - local backup path

### Migration Strategy
- Keep both remotes during transition period
- Gradually migrate to `origin` (Dream.os) as primary
- Use `old-origin` for reference/backup

---

## Remote Management

### Adding Remotes
```bash
# Add remote
git remote add <name> <url>

# Example: Already configured
git remote add old-origin https://github.com/Dadudekc/Agent_Cellphone_V2_Repository.git
```

### Removing Remotes
```bash
# Remove remote
git remote remove <name>
```

### Updating Remote URLs
```bash
# Update remote URL
git remote set-url <name> <new-url>
```

---

## Notes

- **Default remote**: `origin` (Dream.os) is the default for all git operations
- **Explicit access**: Use `old-origin` explicitly to access the old repository
- **Backup strategy**: Both remotes can be used for redundancy
- **Migration**: This setup allows gradual migration from old to new repository

---

*Configuration verified and documented by Agent-6*

