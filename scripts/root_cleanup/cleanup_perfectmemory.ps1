# PerfectMemory Cleanup Script
# Safely clean old images and cache files from PerfectMemory

param(
    [switch]$PreviewOnly = $false,
    [int]$DaysOld = 90,
    [switch]$CleanWhisperCache = $false
)

$perfectMemoryPath = "$env:LOCALAPPDATA\PerfectMemory"

if (-not (Test-Path $perfectMemoryPath)) {
    Write-Host "PerfectMemory folder not found!" -ForegroundColor Red
    exit
}

Write-Host "=== PerfectMemory Cleanup ===" -ForegroundColor Cyan
Write-Host "Path: $perfectMemoryPath`n" -ForegroundColor Gray

$totalSize = 0
$filesToDelete = @()

# Find old image files
Write-Host "[1/3] Scanning for old image files (older than $DaysOld days)..." -ForegroundColor Yellow
$cutoffDate = (Get-Date).AddDays(-$DaysOld)

$imageFiles = Get-ChildItem -Path $perfectMemoryPath -Recurse -Include *.jpg,*.jpeg,*.png -ErrorAction SilentlyContinue | 
    Where-Object { $_.LastWriteTime -lt $cutoffDate }

foreach ($file in $imageFiles) {
    $size = $file.Length
    $totalSize += $size
    $filesToDelete += $file
    if ($PreviewOnly) {
        Write-Host "  Would delete: $($file.Name) ($([math]::Round($size/1MB,2)) MB, Modified: $($file.LastWriteTime))" -ForegroundColor Gray
    }
}

$totalGB = $totalSize / 1GB
Write-Host "  Found $($filesToDelete.Count) old image files totaling $([math]::Round($totalGB,2)) GB" -ForegroundColor $(if ($PreviewOnly) { "Cyan" } else { "Green" })

# Clean Whisper cache if requested
if ($CleanWhisperCache) {
    Write-Host "`n[2/3] Cleaning Whisper model cache..." -ForegroundColor Yellow
    $whisperPath = Join-Path $perfectMemoryPath "Whisper"
    if (Test-Path $whisperPath) {
        $whisperSize = (Get-ChildItem $whisperPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        if ($PreviewOnly) {
            Write-Host "  Would delete: $([math]::Round($whisperSize,2)) GB from Whisper cache" -ForegroundColor Cyan
        } else {
            Remove-Item $whisperPath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  Deleted $([math]::Round($whisperSize,2)) GB from Whisper cache" -ForegroundColor Green
            $totalGB += $whisperSize
        }
    }
} else {
    Write-Host "`n[2/3] Skipping Whisper cache (use -CleanWhisperCache to clean)" -ForegroundColor Gray
}

# Clean IndexDB cache files
Write-Host "`n[3/3] Cleaning IndexDB cache files..." -ForegroundColor Yellow
$indexDBPath = Join-Path $perfectMemoryPath "IndexDB"
if (Test-Path $indexDBPath) {
    $indexFiles = Get-ChildItem $indexDBPath -File -ErrorAction SilentlyContinue | 
        Where-Object { $_.Extension -in @('.pos', '.doc', '.cfs', '.cfe') -and $_.LastWriteTime -lt $cutoffDate }
    $indexSize = ($indexFiles | Measure-Object -Property Length -Sum).Sum / 1GB
    if ($PreviewOnly) {
        Write-Host "  Would delete: $([math]::Round($indexSize,2)) GB from IndexDB cache" -ForegroundColor Cyan
    } else {
        $indexFiles | Remove-Item -Force -ErrorAction SilentlyContinue
        Write-Host "  Deleted $([math]::Round($indexSize,2)) GB from IndexDB cache" -ForegroundColor Green
        $totalGB += $indexSize
    }
}

# Execute deletion if not preview
if (-not $PreviewOnly -and $filesToDelete.Count -gt 0) {
    Write-Host "`nDeleting $($filesToDelete.Count) files..." -ForegroundColor Yellow
    $filesToDelete | Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Host "  Deletion complete!" -ForegroundColor Green
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
if ($PreviewOnly) {
    Write-Host "PREVIEW MODE - No files deleted" -ForegroundColor Yellow
    Write-Host "Total space that would be freed: $([math]::Round($totalGB,2)) GB" -ForegroundColor Cyan
    Write-Host "`nTo actually delete, run without -PreviewOnly:" -ForegroundColor Yellow
    Write-Host "  .\cleanup_perfectmemory.ps1 -DaysOld 90" -ForegroundColor Gray
} else {
    Write-Host "Total space freed: $([math]::Round($totalGB,2)) GB" -ForegroundColor Green
}

Write-Host "`n✅ Done!" -ForegroundColor Green

