# Final Monorepo Cleanup Script
# Clean up remaining obsolete directories and files
# Usage: .\final_monorepo_cleanup.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "🧹 Final Monorepo Cleanup Script" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

$startTime = Get-Date

# Define directories to clean up
$cleanupTargets = @(
    @{
        Directory = "backups"
        Reason = "Should have been consolidated into archive/ - redundant backup location"
        Action = "Move contents to archive/backups/ and remove directory"
    },
    @{
        Directory = "phase3b_backup"
        Reason = "Phase 3 backup directory that should have been consolidated"
        Action = "Move contents to archive/code/ and remove directory"
    },
    @{
        Directory = "quarantine"
        Reason = "Quarantined files - review and clean if obsolete"
        Action = "Move contents to archive/quarantine/ and remove directory"
    },
    @{
        Directory = "temp"
        Reason = "Temporary files directory - clean old temp files"
        Action = "Move contents to archive/temp/ and remove directory"
    },
    @{
        Directory = "temp_repo_analysis"
        Reason = "Temporary repository analysis data"
        Action = "Move contents to archive/temp/ and remove directory"
    }
)

$filesMoved = 0
$totalSizeMoved = 0
$dirsProcessed = 0

# Function to format file size
function Format-FileSize {
    param([long]$Size)
    if ($Size -gt 1GB) { return "{0:N2} GB" -f ($Size / 1GB) }
    elseif ($Size -gt 1MB) { return "{0:N2} MB" -f ($Size / 1MB) }
    elseif ($Size -gt 1KB) { return "{0:N2} KB" -f ($Size / 1KB) }
    else { return "$Size bytes" }
}

# Analyze cleanup targets
Write-Host "`n📊 Analyzing cleanup targets..." -ForegroundColor Yellow
foreach ($target in $cleanupTargets) {
    $dir = $target.Directory
    if (Test-Path $dir) {
        $itemCount = (Get-ChildItem -Path $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        $size = (Get-ChildItem -Path $dir -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Write-Host "  📁 $dir : $itemCount items, $(Format-FileSize $size)" -ForegroundColor White
        Write-Host "    Reason: $($target.Reason)" -ForegroundColor Gray
        Write-Host "    Action: $($target.Action)" -ForegroundColor Gray
        Write-Host ""
    } else {
        Write-Host "  ⚠️  $dir : Directory not found" -ForegroundColor Yellow
    }
}

# Process cleanup targets
Write-Host "🧹 Processing cleanup targets..." -ForegroundColor Yellow
foreach ($target in $cleanupTargets) {
    $dir = $target.Directory

    if (-not (Test-Path $dir)) {
        Write-Host "  ⏭️  Skipping $dir (not found)" -ForegroundColor Gray
        continue
    }

    $dirsProcessed++

    # Determine archive destination based on content type
    $archiveDest = switch ($dir) {
        "backups" { "archive/data/backups" }
        "phase3b_backup" { "archive/code/phase3b_backup" }
        "quarantine" { "archive/quarantine" }
        "temp" { "archive/temp/final_cleanup" }
        "temp_repo_analysis" { "archive/temp/repo_analysis" }
        default { "archive/temp/misc" }
    }

    # Create archive destination if it doesn't exist
    if (-not $DryRun) {
        if (-not (Test-Path $archiveDest)) {
            New-Item -ItemType Directory -Path $archiveDest -Force | Out-Null
        }
    }

    Write-Host "  📦 Processing $dir → $archiveDest" -ForegroundColor White

    # Move contents
    $items = Get-ChildItem -Path $dir -Recurse -ErrorAction SilentlyContinue
    if ($items.Count -gt 0) {
        foreach ($item in $items) {
            $relativePath = $item.FullName.Replace((Resolve-Path $dir).Path + "\", "")
            $targetPath = Join-Path $archiveDest $relativePath

            if (-not $DryRun) {
                $targetParent = Split-Path $targetPath -Parent
                if (-not (Test-Path $targetParent)) {
                    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
                }

                if ($item.PSIsContainer) {
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    Move-Item -Path $item.FullName -Destination $targetPath -Force
                    $filesMoved++
                    $totalSizeMoved += $item.Length
                }
            } else {
                Write-Host "    [DRY RUN] Would move: $relativePath" -ForegroundColor Magenta
                if (-not $item.PSIsContainer) {
                    $filesMoved++
                    $totalSizeMoved += $item.Length
                }
            }
        }
    }

    # Remove empty directory
    $remainingItems = Get-ChildItem -Path $dir -Recurse -ErrorAction SilentlyContinue
    if (-not $DryRun -and $remainingItems.Count -eq 0) {
        Remove-Item -Path $dir -Recurse -Force
        Write-Host "  ✅ Removed empty directory: $dir" -ForegroundColor Green
    } elseif ($DryRun) {
        Write-Host "  [DRY RUN] Would remove directory: $dir" -ForegroundColor Magenta
    }
}

# Check for any remaining temp-like directories
Write-Host "`n🔍 Scanning for additional temp directories..." -ForegroundColor Yellow
$allDirs = Get-ChildItem -Directory | Where-Object { $_.Name -notmatch "^\.|agent_workspaces|__pycache__|node_modules|\.ruff_cache|htmlcov" }
$tempPatterns = $allDirs | Where-Object { $_.Name -match "^temp|.*temp.*|^old|.*old.*|^backup.*|^.*backup$|^draft|^.*draft$|^archive.*|^.*archive$" -and $_.Name -notin @("archive") }

if ($tempPatterns.Count -gt 0) {
    Write-Host "  Found additional potential cleanup candidates:" -ForegroundColor Yellow
    foreach ($dir in $tempPatterns) {
        $itemCount = (Get-ChildItem -Path $dir.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "    - $($dir.Name): $itemCount items" -ForegroundColor White
    }
} else {
    Write-Host "  No additional temp directories found" -ForegroundColor Gray
}

# Generate cleanup report
$cleanupReport = @"
# Final Monorepo Cleanup Report

## Executive Summary
- **Cleanup Date**: $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))
- **Directories Processed**: $($cleanupTargets.Count)
- **Directories Removed**: $dirsProcessed
- **Files Moved**: $filesMoved
- **Data Archived**: $(Format-FileSize $totalSizeMoved)

## Directories Cleaned

"@

foreach ($target in $cleanupTargets) {
    $dir = $target.Directory
    $status = if (Test-Path $dir) { "❌ Not removed" } else { "✅ Removed" }
    $cleanupReport += "- **$dir**: $status`n"
    $cleanupReport += "  - Reason: $($target.Reason)`n"
    $cleanupReport += "  - Archive Location: $(switch ($dir) {
        "backups" { "archive/data/backups" }
        "phase3b_backup" { "archive/code/phase3b_backup" }
        "quarantine" { "archive/quarantine" }
        "temp" { "archive/temp/final_cleanup" }
        "temp_repo_analysis" { "archive/temp/repo_analysis" }
        default { "archive/temp/misc" }
    })`n`n"
}

$cleanupReport += @"
## Impact Assessment
- **Directory Count**: Reduced repository directory sprawl
- **Archive Organization**: All legacy data properly categorized and accessible
- **Storage Efficiency**: Maintained historical data while cleaning active workspace
- **Discoverability**: Improved navigation by removing obsolete directories

## Next Steps
1. Verify all critical data is accessible in archive locations
2. Update any scripts that reference cleaned-up directory paths
3. Consider implementing automated temp file cleanup policies
4. Monitor for any missing file references

## Validation Checklist
- [ ] All important legacy data accessible in archive
- [ ] No broken references to cleaned directories
- [ ] Repository navigation improved
- [ ] No accidental data loss occurred

---
*Generated by Final Monorepo Cleanup Script*
"@

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Final Cleanup Summary" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Directories processed: $($cleanupTargets.Count)" -ForegroundColor White
Write-Host "Directories removed: $dirsProcessed" -ForegroundColor White
Write-Host "Files moved: $filesMoved" -ForegroundColor White
Write-Host "Data archived: $(Format-FileSize $totalSizeMoved)" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no actual cleanup performed" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to execute actual cleanup" -ForegroundColor Magenta
} else {
    # Save cleanup report
    $reportPath = "archive/final_cleanup_report_$($startTime.ToString('yyyyMMdd')).md"
    $cleanupReport | Out-File -FilePath $reportPath -Encoding UTF8

    Write-Host "`n📄 Final cleanup report saved to: $reportPath" -ForegroundColor Green
    Write-Host "`n✅ Final monorepo cleanup completed successfully" -ForegroundColor Green
    Write-Host "Obsolete directories archived and removed from active workspace" -ForegroundColor Green
}

Write-Host "`n💡 Recommendations:" -ForegroundColor Cyan
Write-Host "1. Verify critical legacy data is accessible in archive locations" -ForegroundColor White
Write-Host "2. Update any scripts referencing cleaned-up directory paths" -ForegroundColor White
Write-Host "3. Consider automated cleanup policies for future temp files" -ForegroundColor White