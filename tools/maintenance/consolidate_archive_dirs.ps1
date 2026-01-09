# Archive Directory Consolidation Script
# Consolidates multiple archive/backup directories into organized structure
# Usage: .\consolidate_archive_dirs.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "📦 Archive Directory Consolidation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$startTime = Get-Date

# Define source directories to consolidate
$sourceDirs = @("archives", "backups", "phase3b_backup")
$targetDir = "archive"

# Initialize counters
$totalFilesMoved = 0
$totalSizeMoved = 0
$dirsCreated = 0

# Function to format file size
function Format-FileSize {
    param([long]$Size)
    if ($Size -gt 1GB) { return "{0:N2} GB" -f ($Size / 1GB) }
    elseif ($Size -gt 1MB) { return "{0:N2} MB" -f ($Size / 1MB) }
    elseif ($Size -gt 1KB) { return "{0:N2} KB" -f ($Size / 1KB) }
    else { return "$Size bytes" }
}

# Analyze source directories
Write-Host "`n📊 Analyzing source directories..." -ForegroundColor Yellow
foreach ($dir in $sourceDirs) {
    if (Test-Path $dir) {
        $items = (Get-ChildItem -Path $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        $size = (Get-ChildItem -Path $dir -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Write-Host "  📁 $dir : $items items, $(Format-FileSize $size)" -ForegroundColor White
    } else {
        Write-Host "  ⚠️  $dir : Directory not found" -ForegroundColor Yellow
    }
}

# Create organized subdirectories in target archive
$subDirs = @(
    "repositories",     # Old repository backups
    "data",            # Data backups and exports
    "deployments",     # Deployment artifacts
    "code",            # Code snapshots and backups
    "temp"             # Temporary archives
)

Write-Host "`n📁 Preparing target directory structure..." -ForegroundColor Yellow
foreach ($subDir in $subDirs) {
    $fullPath = Join-Path $targetDir $subDir
    if (-not (Test-Path $fullPath)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        $dirsCreated++
        Write-Host "  ✅ Created: $fullPath" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Exists: $fullPath" -ForegroundColor Gray
    }
}

# Consolidate archives directory (should be mostly empty)
Write-Host "`n🔄 Consolidating archives/ directory..." -ForegroundColor Yellow
$archivesPath = "archives"
if (Test-Path $archivesPath) {
    $items = Get-ChildItem -Path $archivesPath -Recurse -ErrorAction SilentlyContinue
    if ($items.Count -gt 0) {
        foreach ($item in $items) {
            $relativePath = $item.FullName.Replace((Resolve-Path $archivesPath).Path + "\", "")
            $targetPath = Join-Path $targetDir "temp\$relativePath"

            if (-not $DryRun) {
                $targetParent = Split-Path $targetPath -Parent
                if (-not (Test-Path $targetParent)) {
                    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
                }

                if ($item.PSIsContainer) {
                    # Create directory
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    # Move file
                    Move-Item -Path $item.FullName -Destination $targetPath -Force
                    $totalFilesMoved++
                    $totalSizeMoved += $item.Length
                }
            } else {
                Write-Host "  [DRY RUN] Would move: $($item.FullName) → $targetPath" -ForegroundColor Magenta
                if (-not $item.PSIsContainer) {
                    $totalFilesMoved++
                    $totalSizeMoved += $item.Length
                }
            }
        }
    }

    # Remove empty archives directory
    if (-not $DryRun -and (Get-ChildItem -Path $archivesPath -Recurse | Measure-Object).Count -eq 0) {
        Remove-Item -Path $archivesPath -Recurse -Force
        Write-Host "  ✅ Removed empty: $archivesPath" -ForegroundColor Green
    }
}

# Consolidate phase3b_backup directory
Write-Host "`n🔄 Consolidating phase3b_backup/ directory..." -ForegroundColor Yellow
$phase3bPath = "phase3b_backup"
if (Test-Path $phase3bPath) {
    $items = Get-ChildItem -Path $phase3bPath -Recurse -ErrorAction SilentlyContinue
    if ($items.Count -gt 0) {
        foreach ($item in $items) {
            $relativePath = $item.FullName.Replace((Resolve-Path $phase3bPath).Path + "\", "")
            $targetPath = Join-Path $targetDir "code\$relativePath"

            if (-not $DryRun) {
                $targetParent = Split-Path $targetPath -Parent
                if (-not (Test-Path $targetParent)) {
                    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
                }

                if ($item.PSIsContainer) {
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    Move-Item -Path $item.FullName -Destination $targetPath -Force
                    $totalFilesMoved++
                    $totalSizeMoved += $item.Length
                }
            } else {
                Write-Host "  [DRY RUN] Would move: $($item.FullName) → $targetPath" -ForegroundColor Magenta
                if (-not $item.PSIsContainer) {
                    $totalFilesMoved++
                    $totalSizeMoved += $item.Length
                }
            }
        }
    }

    # Remove empty phase3b_backup directory
    if (-not $DryRun -and (Get-ChildItem -Path $phase3bPath -Recurse | Measure-Object).Count -eq 0) {
        Remove-Item -Path $phase3bPath -Recurse -Force
        Write-Host "  ✅ Removed empty: $phase3bPath" -ForegroundColor Green
    }
}

# Consolidate backups directory (more complex, categorize by content)
Write-Host "`n🔄 Consolidating backups/ directory..." -ForegroundColor Yellow
$backupsPath = "backups"
if (Test-Path $backupsPath) {
    $items = Get-ChildItem -Path $backupsPath -Recurse -ErrorAction SilentlyContinue
    if ($items.Count -gt 0) {
        foreach ($item in $items) {
            $itemName = $item.Name.ToLower()

            # Categorize by content type
            if ($itemName -match "deploy|site|web") {
                $category = "deployments"
            } elseif ($itemName -match "data|db|database") {
                $category = "data"
            } elseif ($itemName -match "repo|git|code") {
                $category = "repositories"
            } else {
                $category = "data"  # Default category
            }

            $relativePath = $item.FullName.Replace((Resolve-Path $backupsPath).Path + "\", "")
            $targetPath = Join-Path $targetDir "$category\$relativePath"

            if (-not $DryRun) {
                $targetParent = Split-Path $targetPath -Parent
                if (-not (Test-Path $targetParent)) {
                    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
                }

                if ($item.PSIsContainer) {
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    Move-Item -Path $item.FullName -Destination $targetPath -Force
                    $totalFilesMoved++
                    $totalSizeMoved += $item.Length
                }
            } else {
                Write-Host "  [DRY RUN] Would move: $($item.FullName) → $targetPath" -ForegroundColor Magenta
                if (-not $item.PSIsContainer) {
                    $totalFilesMoved++
                    $totalSizeMoved += $item.Length
                }
            }
        }
    }

    # Note: Keep backups directory as it may be actively used, just consolidate contents
    Write-Host "  ℹ️  Kept backups/ directory (may be actively used)" -ForegroundColor Yellow
}

# Create consolidation report
$consolidationReport = @"
# Archive Directory Consolidation Report

## Executive Summary
- **Consolidation Date**: $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))
- **Directories Processed**: archives/, phase3b_backup/, backups/
- **Files Consolidated**: $totalFilesMoved
- **Data Moved**: $(Format-FileSize $totalSizeMoved)
- **New Subdirectories Created**: $dirsCreated

## Consolidation Details

### Source Directories
- **archives/**: Merged into archive/temp/
- **phase3b_backup/**: Merged into archive/code/ (removed after consolidation)
- **backups/**: Categorized and merged into archive/data/, archive/deployments/, etc.

### Target Structure
```
archive/
├── repositories/     # Repository backups
├── data/            # Data and database backups
├── deployments/     # Web and deployment backups
├── code/            # Code snapshots and phase backups
└── temp/            # Miscellaneous archives
```

## Next Steps
1. Verify all critical backups are accessible in new locations
2. Update any scripts that reference old backup paths
3. Consider implementing automated cleanup policies
4. Monitor for any missing backup references

## Validation Checklist
- [ ] All important backups accessible in new structure
- [ ] No broken references to old backup locations
- [ ] Directory structure logical and discoverable
- [ ] Cleanup completed without data loss

---
*Generated by Archive Consolidation Script*
"@

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Archive Consolidation Summary" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Files moved: $totalFilesMoved" -ForegroundColor White
Write-Host "Data moved: $(Format-FileSize $totalSizeMoved)" -ForegroundColor White
Write-Host "Directories created: $dirsCreated" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no actual consolidation performed" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to execute actual consolidation" -ForegroundColor Magenta
} else {
    # Save consolidation report
    $reportPath = "archive/consolidation_report_$($startTime.ToString('yyyyMMdd')).md"
    $consolidationReport | Out-File -FilePath $reportPath -Encoding UTF8

    Write-Host "`n📄 Consolidation report saved to: $reportPath" -ForegroundColor Green
    Write-Host "`n✅ Archive directory consolidation completed successfully" -ForegroundColor Green
    Write-Host "Multiple backup directories merged into organized archive structure" -ForegroundColor Green
}

Write-Host "`n💡 Recommendations:" -ForegroundColor Cyan
Write-Host "1. Verify critical backups are accessible in new locations" -ForegroundColor White
Write-Host "2. Update scripts referencing old backup paths" -ForegroundColor White
Write-Host "3. Consider automated archive cleanup policies" -ForegroundColor White