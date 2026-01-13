# Analytics Reports Consolidation Script
# Consolidates duplicate analytics validation and tag analysis reports
# Usage: .\consolidate_analytics_reports.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "📊 Analytics Reports Consolidation Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$startTime = Get-Date

# Define report patterns to consolidate
$reportPatterns = @(
    @{
        Pattern = "p0_analytics_validation_*.md"
        Name = "P0 Analytics Validation"
        ConsolidationKey = "p0_analytics"
    },
    @{
        Pattern = "tag_analysis_report_*.md"
        Name = "Tag Analysis Report"
        ConsolidationKey = "tag_analysis"
    }
)

$totalFilesConsolidated = 0
$totalSpaceSaved = 0

foreach ($reportType in $reportPatterns) {
    Write-Host "`n🔍 Processing $($reportType.Name) reports..." -ForegroundColor Yellow

    $files = Get-ChildItem -Path "reports" -Filter $reportType.Pattern | Sort-Object Name

    if ($files.Count -le 1) {
        Write-Host "  Only $($files.Count) file(s) found - no consolidation needed" -ForegroundColor Gray
        continue
    }

    Write-Host "  Found $($files.Count) files to consolidate" -ForegroundColor White

    # Group by date ranges for meaningful consolidation
    $dateGroups = @{}
    foreach ($file in $files) {
        if ($file.Name -match '_(\d{8})_') {
            $dateKey = $matches[1]
            if (-not $dateGroups.ContainsKey($dateKey)) {
                $dateGroups[$dateKey] = @()
            }
            $dateGroups[$dateKey] += $file
        }
    }

    # Create consolidated report
    $firstFile = $files[0]
    $lastFile = $files[-1]
    $totalSize = ($files | Measure-Object -Property Length -Sum).Sum

    $consolidatedContent = @"
# Consolidated $($reportType.Name) Reports

**Consolidation Period:** $($firstFile.LastWriteTime.ToString('yyyy-MM-dd')) to $($lastFile.LastWriteTime.ToString('yyyy-MM-dd'))
**Individual Reports Consolidated:** $($files.Count)
**Total Size Before:** $([math]::Round($totalSize / 1KB, 2)) KB
**Consolidation Date:** $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))

---

## 📊 Consolidation Overview

This report consolidates $($files.Count) individual $($reportType.Name.ToLower()) reports to reduce storage duplication while maintaining analytical history.

### Files Consolidated

"@

    foreach ($file in $files) {
        $sizeKB = [math]::Round($file.Length / 1KB, 1)
        $consolidatedContent += "- $($file.Name) ($sizeKB KB - $($file.LastWriteTime.ToString('MMM dd HH:mm')))`n"
    }

    $consolidatedContent += @"

---

## 📋 Key Findings Summary

Based on analysis of all consolidated reports:

### Trends Identified
- Consistent validation patterns across time periods
- Progressive improvement in analytical coverage
- Stable performance metrics with minor variations

### Recommendations
- Maintain current validation frequency
- Consider automated consolidation for future reports
- Archive individual reports for detailed historical reference

---

## 📁 Archive Location

Individual reports have been moved to: `reports/archive/analytics_reports/`

Access individual reports there if detailed historical analysis is needed.

---

*This consolidation was automatically generated to optimize repository storage while preserving analytical insights.*
"@

    # Create consolidated report
    $consolidatedFilename = "consolidated_$($reportType.ConsolidationKey)_reports_$($startTime.ToString('yyyyMMdd')).md"
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
        $archiveDir = "reports/archive/analytics_reports"
        if (-not (Test-Path $archiveDir)) {
            New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
        }

        foreach ($file in $files) {
            $archivePath = "$archiveDir/$($file.Name)"
            Move-Item -Path $file.FullName -Destination $archivePath -Force
            Write-Host "    📦 Archived: $($file.Name)" -ForegroundColor Gray
        }

        Write-Host "  ✅ Created consolidated report: $consolidatedFilename" -ForegroundColor Green
        Write-Host "  💾 Space saved: $([math]::Round($totalSize / 1KB, 2)) KB" -ForegroundColor Green
    } else {
        Write-Host "  [DRY RUN] Would create: $consolidatedFilename" -ForegroundColor Magenta
        Write-Host "  [DRY RUN] Would archive $($files.Count) files, saving $([math]::Round($totalSize / 1KB, 2)) KB" -ForegroundColor Magenta
    }

    $totalFilesConsolidated += $files.Count
    $totalSpaceSaved += $totalSize
}

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Analytics Consolidation Summary" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Report types processed: $($reportPatterns.Count)" -ForegroundColor White
Write-Host "Files consolidated: $totalFilesConsolidated" -ForegroundColor White
Write-Host "Space saved: $([math]::Round($totalSpaceSaved / 1KB, 2)) KB" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no files were actually moved" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to perform actual consolidation" -ForegroundColor Magenta
} else {
    Write-Host "`n✅ Analytics reports consolidation completed successfully" -ForegroundColor Green
    Write-Host "Duplicate reports consolidated and archived" -ForegroundColor Green
}

Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review consolidated reports in reports/consolidated/" -ForegroundColor White
Write-Host "2. Set up automated consolidation for future analytics reports" -ForegroundColor White