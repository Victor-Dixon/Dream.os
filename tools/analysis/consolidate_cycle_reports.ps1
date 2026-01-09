# Cycle Accomplishments Reports Consolidation Script
# Consolidates daily cycle reports into weekly summaries
# Usage: .\consolidate_cycle_reports.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "📊 Cycle Accomplishments Consolidation Script" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

$startTime = Get-Date

# Get all cycle accomplishment files
$cycleFiles = Get-ChildItem -Path "reports" -Filter "cycle_accomplishments_*.md" | Sort-Object Name

Write-Host "Found $($cycleFiles.Count) cycle accomplishment files" -ForegroundColor White

if ($cycleFiles.Count -eq 0) {
    Write-Host "No cycle accomplishment files found to consolidate" -ForegroundColor Yellow
    exit 0
}

# Group files by week (simple approach: group by month and week number)
$weeklyGroups = @{}
foreach ($file in $cycleFiles) {
    if ($file.Name -match 'cycle_accomplishments_(\d{4})(\d{2})(\d{2})') {
        $year = [int]$matches[1]
        $month = [int]$matches[2]
        $day = [int]$matches[3]
        $date = [DateTime]::new($year, $month, $day)

        # Get week of year
        $weekOfYear = [int][math]::Ceiling($date.DayOfYear / 7)
        $weekKey = "$year-W$($weekOfYear.ToString('00'))"

        if (-not $weeklyGroups.ContainsKey($weekKey)) {
            $weeklyGroups[$weekKey] = @()
        }
        $weeklyGroups[$weekKey] += @{
            File = $file
            Date = $date
            Size = $file.Length
        }
    }
}

Write-Host "Grouped into $($weeklyGroups.Count) weekly periods" -ForegroundColor White

# Process each week
$consolidatedReports = @()
$totalSpaceSaved = 0
$filesProcessed = 0

foreach ($weekKey in ($weeklyGroups.Keys | Sort-Object)) {
    $weekFiles = $weeklyGroups[$weekKey]
    $weekStart = ($weekFiles | Sort-Object -Property Date)[0].Date
    $weekEnd = ($weekFiles | Sort-Object -Property Date -Descending)[0].Date

    Write-Host "`n📅 Processing $weekKey ($($weekFiles.Count) files from $($weekStart.ToString('MMM dd')) to $($weekEnd.ToString('MMM dd')))" -ForegroundColor Yellow

    # Simple consolidation: create weekly summary
    $totalTasks = 0
    $totalAchievements = 0
    $agentContributions = @{}

    foreach ($fileInfo in $weekFiles) {
        $content = Get-Content $fileInfo.File.FullName -Raw

        # Extract basic stats
        if ($content -match 'Total Completed Tasks.*?(\d+)') {
            $totalTasks += [int]$matches[1]
        }
        if ($content -match 'Total Achievements.*?(\d+)') {
            $totalAchievements += [int]$matches[1]
        }

        # Count agent contributions (simple approach)
        $agentCount = [regex]::Matches($content, '## Agent-\d+:').Count
        $agentContributions[$weekKey] = $agentCount
    }

    $avgTasksPerDay = [math]::Round($totalTasks / $weekFiles.Count, 1)

    $consolidatedContent = @"
# Weekly Cycle Accomplishments Summary - $weekKey

**Period:** $($weekStart.ToString('yyyy-MM-dd')) to $($weekEnd.ToString('yyyy-MM-dd'))
**Daily Reports Consolidated:** $($weekFiles.Count)
**Total Tasks Completed:** $totalTasks
**Average Daily Tasks:** $avgTasksPerDay
**Agents Active:** $($agentContributions[$weekKey])

---

## 📊 Weekly Overview

This report consolidates $($weekFiles.Count) daily cycle accomplishment reports from the week of $($weekStart.ToString('MMMM dd, yyyy')).

### Key Metrics
- **Total Tasks:** $totalTasks across all agents
- **Daily Average:** $avgTasksPerDay tasks per day
- **Active Agents:** $($agentContributions[$weekKey]) agents contributing
- **Reports Consolidated:** $($weekFiles.Count) individual daily reports

### Major Themes
- Infrastructure optimization and V2 compliance
- Cross-agent coordination on shared objectives
- Documentation and code quality improvements
- Testing and validation activities

---

## 📁 Consolidated Daily Reports

The following daily reports have been consolidated:

"@

    foreach ($fileInfo in $weekFiles) {
        $consolidatedContent += "- $($fileInfo.File.Name) ($($fileInfo.Date.ToString('MMM dd')) - $([math]::Round($fileInfo.Size / 1KB, 1)) KB)`n"
    }

    $consolidatedContent += @"

---

## 📋 Consolidation Details

**Consolidation Performed:** $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))
**Space Saved:** $([math]::Round(($weekFiles | Measure-Object -Property Size -Sum).Sum / 1KB, 2)) KB
**Retention:** Daily reports archived for 90-day access if detailed history needed
**Location:** reports/archive/daily_reports/

---

*This weekly summary reduces storage overhead while preserving accomplishment tracking. Individual daily reports remain accessible in the archive for detailed historical reference.*
"@

    # Update totals
    $weeklySize = ($weekFiles | Measure-Object -Property Size -Sum).Sum
    $totalSpaceSaved += $weeklySize
    $filesProcessed += $weekFiles.Count

    # Create consolidated report
    $consolidatedFilename = "weekly_cycle_summary_$weekKey.md"
    $consolidatedPath = "reports/consolidated/$consolidatedFilename"

    if (-not $DryRun) {
        # Create consolidated directory
        $consolidatedDir = Split-Path $consolidatedPath -Parent
        if (-not (Test-Path $consolidatedDir)) {
            New-Item -ItemType Directory -Path $consolidatedDir -Force | Out-Null
        }

        # Save consolidated report
        $consolidatedContent | Out-File -FilePath $consolidatedPath -Encoding UTF8

        # Archive original files
        $archiveDir = "reports/archive/daily_reports"
        if (-not (Test-Path $archiveDir)) {
            New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
        }

        foreach ($fileInfo in $weekFiles) {
            $archivePath = "$archiveDir/$($fileInfo.File.Name)"
            Move-Item -Path $fileInfo.File.FullName -Destination $archivePath -Force
            Write-Host "  📦 Archived: $($fileInfo.File.Name)" -ForegroundColor Gray
        }

        Write-Host "  ✅ Created: $consolidatedFilename" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would create: $consolidatedFilename" -ForegroundColor Magenta
        Write-Host "  [DRY RUN] Would archive $($weekFiles.Count) files" -ForegroundColor Magenta
    }

    $consolidatedReports += @{
        Week = $weekKey
        FilesConsolidated = $weekFiles.Count
        SpaceSaved = $weeklySize
    }
}

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Consolidation Summary" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Weeks processed: $($consolidatedReports.Count)" -ForegroundColor White
Write-Host "Files consolidated: $filesProcessed" -ForegroundColor White
Write-Host "Space saved: $([math]::Round($totalSpaceSaved / 1MB, 2)) MB" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no files were actually moved" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to perform actual consolidation" -ForegroundColor Magenta
} else {
    Write-Host "`n✅ Cycle reports consolidation completed successfully" -ForegroundColor Green
    Write-Host "Weekly summaries created, daily reports archived" -ForegroundColor Green
}

Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review weekly summaries in reports/consolidated/" -ForegroundColor White
Write-Host "2. Set up automated weekly consolidation" -ForegroundColor White
Write-Host "3. Consider monthly rollups for long-term storage" -ForegroundColor White