# Infrastructure Cache Cleanup Script
# Removes Python cache files and build artifacts to optimize repository size
# Usage: .\cleanup_cache_files.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "🧹 Infrastructure Cache Cleanup Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$startTime = Get-Date
$filesRemoved = 0
$spaceSaved = 0

# Function to format file size
function Format-FileSize {
    param([long]$Size)
    if ($Size -gt 1GB) { return "{0:N2} GB" -f ($Size / 1GB) }
    elseif ($Size -gt 1MB) { return "{0:N2} MB" -f ($Size / 1MB) }
    elseif ($Size -gt 1KB) { return "{0:N2} KB" -f ($Size / 1KB) }
    else { return "$Size bytes" }
}

# Clean .pyc files
Write-Host "`n🗂️  Cleaning Python cache files (.pyc)..." -ForegroundColor Yellow
$pycFiles = Get-ChildItem -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue
if ($pycFiles) {
    $pycSize = ($pycFiles | Measure-Object -Property Length -Sum).Sum
    Write-Host "Found $($pycFiles.Count) .pyc files using $(Format-FileSize $pycSize)" -ForegroundColor Gray

    if ($DryRun) {
        Write-Host "[DRY RUN] Would remove $($pycFiles.Count) .pyc files" -ForegroundColor Magenta
    } else {
        $pycFiles | Remove-Item -Force
        Write-Host "✅ Removed $($pycFiles.Count) .pyc files" -ForegroundColor Green
        $filesRemoved += $pycFiles.Count
        $spaceSaved += $pycSize
    }
} else {
    Write-Host "No .pyc files found" -ForegroundColor Gray
}

# Clean __pycache__ directories
Write-Host "`n📁 Cleaning __pycache__ directories..." -ForegroundColor Yellow
$pycacheDirs = Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
if ($pycacheDirs) {
    Write-Host "Found $($pycacheDirs.Count) __pycache__ directories" -ForegroundColor Gray

    if ($DryRun) {
        Write-Host "[DRY RUN] Would remove $($pycacheDirs.Count) __pycache__ directories" -ForegroundColor Magenta
    } else {
        $pycacheDirs | Remove-Item -Recurse -Force
        Write-Host "✅ Removed $($pycacheDirs.Count) __pycache__ directories" -ForegroundColor Green
    }
} else {
    Write-Host "No __pycache__ directories found" -ForegroundColor Gray
}

# Clean .ruff_cache directory
Write-Host "`n🔧 Cleaning .ruff_cache directory..." -ForegroundColor Yellow
$ruffCachePath = ".\.ruff_cache"
if (Test-Path $ruffCachePath) {
    $ruffCacheSize = (Get-ChildItem -Recurse -Path $ruffCachePath -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "Found .ruff_cache directory using $(Format-FileSize $ruffCacheSize)" -ForegroundColor Gray

    if ($DryRun) {
        Write-Host "[DRY RUN] Would remove .ruff_cache directory" -ForegroundColor Magenta
    } else {
        Remove-Item -Recurse -Force $ruffCachePath
        Write-Host "✅ Removed .ruff_cache directory" -ForegroundColor Green
        $spaceSaved += $ruffCacheSize
    }
} else {
    Write-Host "No .ruff_cache directory found" -ForegroundColor Gray
}

# Clean other common cache directories
$cacheDirs = @(
    "node_modules/.cache",
    ".next/cache",
    ".nuxt/cache",
    "target/surefire-reports",  # Maven test reports
    "build/test-results",       # Gradle test results
    ".pytest_cache",
    ".mypy_cache"
)

foreach ($cacheDir in $cacheDirs) {
    if (Test-Path $cacheDir) {
        Write-Host "`n🗂️  Cleaning $cacheDir..." -ForegroundColor Yellow
        $cacheSize = (Get-ChildItem -Recurse -Path $cacheDir -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Write-Host "Found cache directory using $(Format-FileSize $cacheSize)" -ForegroundColor Gray

        if ($DryRun) {
            Write-Host "[DRY RUN] Would remove $cacheDir" -ForegroundColor Magenta
        } else {
            Remove-Item -Recurse -Force $cacheDir
            Write-Host "✅ Removed $cacheDir" -ForegroundColor Green
            $spaceSaved += $cacheSize
        }
    }
}

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Cleanup Summary" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Files removed: $filesRemoved" -ForegroundColor White
Write-Host "Space saved: $(Format-FileSize $spaceSaved)" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no files were actually removed" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to perform actual cleanup" -ForegroundColor Magenta
} else {
    Write-Host "`n✅ Cache cleanup completed successfully" -ForegroundColor Green
    Write-Host "Repository size optimized for better performance" -ForegroundColor Green
}

Write-Host "`n💡 Recommendation: Add this script to your CI/CD pipeline for automated cleanup" -ForegroundColor Cyan