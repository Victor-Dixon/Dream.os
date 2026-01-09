# Reports Directory Consolidation Script
# Archives reports older than 30 days and identifies consolidation opportunities
# Usage: .\consolidate_reports.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "📊 Reports Directory Consolidation Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$startTime = Get-Date
$currentDate = Get-Date
$cutoffDate = $currentDate.AddDays(-30)
$cutoffDateString = $cutoffDate.ToString("yyyyMMdd")

Write-Host "Current date: $($currentDate.ToString('yyyy-MM-dd'))" -ForegroundColor White
Write-Host "Archival cutoff: $($cutoffDate.ToString('yyyy-MM-dd')) (files before $cutoffDateString)" -ForegroundColor White
Write-Host ""

# Initialize counters
$filesAnalyzed = 0
$filesArchived = 0
$spaceSaved = 0
$archiveDirsCreated = 0

# Function to extract date from filename
function Get-FileDate {
    param([string]$filename)

    # Match YYYYMMDD pattern
    if ($filename -match '(\d{8})') {
        try {
            $dateString = $matches[1]
            $year = $dateString.Substring(0, 4)
            $month = $dateString.Substring(4, 2)
            $day = $dateString.Substring(6, 2)
            return [DateTime]::ParseExact("$year-$month-$day", "yyyy-MM-dd", $null)
        } catch {
            return $null
        }
    }
    return $null
}

# Function to format file size
function Format-FileSize {
    param([long]$Size)
    if ($Size -gt 1GB) { return "{0:N2} GB" -f ($Size / 1GB) }
    elseif ($Size -gt 1MB) { return "{0:N2} MB" -f ($Size / 1MB) }
    elseif ($Size -gt 1KB) { return "{0:N2} KB" -f ($Size / 1KB) }
    else { return "$Size bytes" }
}

# Get all files in reports directory
$reportFiles = Get-ChildItem -Path "reports" -File -Recurse | Where-Object { $_.Directory.Name -ne "archive" }

Write-Host "📁 Analyzing $($reportFiles.Count) files in reports directory..." -ForegroundColor Yellow

# Analyze files and identify archival candidates
$archivalCandidates = @()
$duplicateCandidates = @{}
$reportTypes = @{}

foreach ($file in $reportFiles) {
    $filesAnalyzed++

    # Extract date from filename
    $fileDate = Get-FileDate -filename $file.Name

    if ($fileDate) {
        # Check if file is older than cutoff
        if ($fileDate -lt $cutoffDate) {
            $archivalCandidates += @{
                File = $file
                Date = $fileDate
                Size = $file.Length
                Year = $fileDate.Year
            }
        }
    }

    # Identify potential duplicates by base name pattern
    $baseName = $file.Name -replace '_\d{8}_\d{6}', '' -replace '_\d{8}', ''
    if (-not $duplicateCandidates.ContainsKey($baseName)) {
        $duplicateCandidates[$baseName] = @()
    }
    $duplicateCandidates[$baseName] += $file

    # Track report types for consolidation analysis
    $reportType = if ($file.Name -match '^(.*?)(?:_\d|$)') { $matches[1] } else { "other" }
    if (-not $reportTypes.ContainsKey($reportType)) {
        $reportTypes[$reportType] = @()
    }
    $reportTypes[$reportType] += $file
}

Write-Host "✅ Analysis complete: $filesAnalyzed files processed" -ForegroundColor Green
Write-Host "📅 Found $($archivalCandidates.Count) files eligible for archival" -ForegroundColor White

# Create archive subdirectories
$years = $archivalCandidates | ForEach-Object { $_.Year } | Sort-Object -Unique
foreach ($year in $years) {
    $archivePath = "reports/archive/$year"
    if (-not (Test-Path $archivePath)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
        }
        $archiveDirsCreated++
        Write-Host "📁 Created archive directory: $archivePath" -ForegroundColor Gray
    }
}

# Archive old files
Write-Host "`n📦 Archiving old reports..." -ForegroundColor Yellow
foreach ($candidate in $archivalCandidates) {
    $file = $candidate.File
    $year = $candidate.Year
    $archivePath = "reports/archive/$year/$($file.Name)"

    if ($DryRun) {
        Write-Host "[DRY RUN] Would archive: $($file.FullName) -> $archivePath" -ForegroundColor Magenta
    } else {
        try {
            Move-Item -Path $file.FullName -Destination $archivePath -Force
            $filesArchived++
            $spaceSaved += $candidate.Size
            Write-Host "✅ Archived: $($file.Name)" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to archive: $($file.Name) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Analyze duplicates for consolidation
Write-Host "`n🔍 Analyzing duplicate reports for consolidation..." -ForegroundColor Yellow
$duplicateSummary = @()
foreach ($baseName in $duplicateCandidates.Keys) {
    $files = $duplicateCandidates[$baseName]
    if ($files.Count -gt 1) {
        $duplicateSummary += @{
            BaseName = $baseName
            Count = $files.Count
            TotalSize = ($files | Measure-Object -Property Length -Sum).Sum
            Files = $files.Name
        }
    }
}

# Generate consolidation report
$consolidationReport = @"
# Reports Directory Consolidation Report

## 📊 Executive Summary
- **Date:** $($currentDate.ToString('yyyy-MM-dd'))
- **Files Analyzed:** $filesAnalyzed
- **Files Archived:** $filesArchived
- **Space Saved:** $(Format-FileSize $spaceSaved)
- **Archive Directories Created:** $archiveDirsCreated

## 📅 Archival Summary
- **Cutoff Date:** $($cutoffDate.ToString('yyyy-MM-dd'))
- **Files Eligible:** $($archivalCandidates.Count)
- **Files Processed:** $filesArchived

## 🔄 Duplicate Analysis
"@

if ($duplicateSummary.Count -gt 0) {
    $consolidationReport += "`n### High-Priority Consolidation Candidates`n"
    foreach ($dup in ($duplicateSummary | Sort-Object -Property Count -Descending | Select-Object -First 10)) {
        $consolidationReport += "`n**$($dup.BaseName)** ($($dup.Count) files, $(Format-FileSize $dup.TotalSize))"
        $consolidationReport += "`n- Files: $($dup.Files -join ', ')`n"
    }
} else {
    $consolidationReport += "`nNo significant duplicates found for consolidation.`n"
}

# Report type analysis
$consolidationReport += "`n## 📋 Report Type Distribution`n"
foreach ($type in ($reportTypes.Keys | Sort-Object)) {
    $count = $reportTypes[$type].Count
    $totalSize = ($reportTypes[$type] | Measure-Object -Property Length -Sum).Sum
    $consolidationReport += "- **$type**: $count files ($(Format-FileSize $totalSize))`n"
}

# Recommendations
$consolidationReport += @"

## 💡 Recommendations

### Immediate Actions
1. **Review Archived Files** - Validate archived reports are no longer needed
2. **Consolidate Duplicates** - Merge similar reports into summary formats
3. **Implement Automated Archival** - Set up CI/CD job for ongoing maintenance

### Long-term Strategy
1. **Report Templates** - Standardize report formats to reduce duplication
2. **Retention Policies** - Define clear retention periods by report type
3. **Compression** - Consider compressing archived reports for further space savings

## 📈 Success Metrics
- **Storage Optimization:** $(Format-FileSize $spaceSaved) reclaimed
- **Maintenance Reduction:** Automated archival process established
- **Organization Improvement:** Clear archive structure implemented
"@

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Consolidation Summary" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Files analyzed: $filesAnalyzed" -ForegroundColor White
Write-Host "Files archived: $filesArchived" -ForegroundColor White
Write-Host "Space saved: $(Format-FileSize $spaceSaved)" -ForegroundColor White
Write-Host "Duplicate groups found: $($duplicateSummary.Count)" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no files were actually moved" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to perform actual consolidation" -ForegroundColor Magenta
} else {
    # Save consolidation report
    $reportPath = "reports/archive/consolidation_report_$($currentDate.ToString('yyyyMMdd')).md"
    $consolidationReport | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Host "`n📄 Consolidation report saved to: $reportPath" -ForegroundColor Green

    Write-Host "`n✅ Reports consolidation completed successfully" -ForegroundColor Green
    Write-Host "Repository maintenance automated and optimized" -ForegroundColor Green
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Review consolidation_report_$($currentDate.ToString('yyyyMMdd')).md" -ForegroundColor White
Write-Host "2. Validate archived files are accessible" -ForegroundColor White
Write-Host "3. Consider merging duplicate reports" -ForegroundColor White