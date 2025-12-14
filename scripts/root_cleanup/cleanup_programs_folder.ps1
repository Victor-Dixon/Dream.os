# Programs Folder Cleanup Script
# Safely clean cache and unused programs from LocalAppData\Programs

param(
    [switch]$PreviewOnly = $false,
    [switch]$CleanPythonCache = $false,
    [switch]$CleanVSCode = $false,
    [switch]$CleanParadox = $false,
    [switch]$CleanOllamaModels = $false
)

Write-Host "=== Programs Folder Cleanup ===" -ForegroundColor Cyan
Write-Host "Path: $env:LOCALAPPDATA\Programs`n" -ForegroundColor Gray

$totalFreed = 0

# 1. Python pip cache cleanup
if ($CleanPythonCache) {
    Write-Host "[1/5] Cleaning Python pip cache..." -ForegroundColor Yellow
    $pipCache = "$env:LOCALAPPDATA\pip\cache"
    if (Test-Path $pipCache) {
        $before = (Get-ChildItem $pipCache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        if ($PreviewOnly) {
            Write-Host "  Would free: $([math]::Round($before,2)) GB from pip cache" -ForegroundColor Cyan
            $totalFreed += $before
        } else {
            Remove-Item $pipCache -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  Freed: $([math]::Round($before,2)) GB from pip cache" -ForegroundColor Green
            $totalFreed += $before
        }
    }
} else {
    Write-Host "[1/5] Skipping Python cache (use -CleanPythonCache)" -ForegroundColor Gray
}

# 2. VS Code removal (if using Cursor)
if ($CleanVSCode) {
    Write-Host "`n[2/5] Removing Microsoft VS Code..." -ForegroundColor Yellow
    $vscodePath = "$env:LOCALAPPDATA\Programs\Microsoft VS Code"
    if (Test-Path $vscodePath) {
        $before = (Get-ChildItem $vscodePath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        if ($PreviewOnly) {
            Write-Host "  Would free: $([math]::Round($before,2)) GB by removing VS Code" -ForegroundColor Cyan
            Write-Host "  Note: You're using Cursor, so VS Code may be redundant" -ForegroundColor Gray
            $totalFreed += $before
        } else {
            Remove-Item $vscodePath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  Freed: $([math]::Round($before,2)) GB by removing VS Code" -ForegroundColor Green
            $totalFreed += $before
        }
    } else {
        Write-Host "  VS Code not found" -ForegroundColor Gray
    }
} else {
    Write-Host "`n[2/5] Skipping VS Code (use -CleanVSCode to remove)" -ForegroundColor Gray
}

# 3. Paradox Interactive removal
if ($CleanParadox) {
    Write-Host "`n[3/5] Removing Paradox Interactive..." -ForegroundColor Yellow
    $paradoxPath = "$env:LOCALAPPDATA\Programs\Paradox Interactive"
    if (Test-Path $paradoxPath) {
        $before = (Get-ChildItem $paradoxPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        if ($PreviewOnly) {
            Write-Host "  Would free: $([math]::Round($before,2)) GB by removing Paradox Interactive" -ForegroundColor Cyan
            Write-Host "  Note: Game launcher - remove if you don't play Paradox games" -ForegroundColor Gray
            $totalFreed += $before
        } else {
            Remove-Item $paradoxPath -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "  Freed: $([math]::Round($before,2)) GB by removing Paradox Interactive" -ForegroundColor Green
            $totalFreed += $before
        }
    } else {
        Write-Host "  Paradox Interactive not found" -ForegroundColor Gray
    }
} else {
    Write-Host "`n[3/5] Skipping Paradox Interactive (use -CleanParadox to remove)" -ForegroundColor Gray
}

# 4. Ollama models cleanup
if ($CleanOllamaModels) {
    Write-Host "`n[4/5] Cleaning Ollama models..." -ForegroundColor Yellow
    $ollamaModelsPath = "$env:USERPROFILE\.ollama\models"
    if (Test-Path $ollamaModelsPath) {
        Write-Host "  WARNING: This will list models for manual review" -ForegroundColor Red
        Get-ChildItem $ollamaModelsPath -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
            Write-Host "  Model: $($_.Name) - $([math]::Round($size,2)) GB" -ForegroundColor Gray
        }
        Write-Host "  Note: Delete models manually from: $ollamaModelsPath" -ForegroundColor Yellow
    } else {
        Write-Host "  Ollama models folder not found" -ForegroundColor Gray
    }
} else {
    Write-Host "`n[4/5] Skipping Ollama models (use -CleanOllamaModels to review)" -ForegroundColor Gray
}

# 5. Check for empty directories
Write-Host "`n[5/5] Checking for empty directories..." -ForegroundColor Yellow
$programsPath = "$env:LOCALAPPDATA\Programs"
$emptyDirs = Get-ChildItem $programsPath -Directory -ErrorAction SilentlyContinue | 
    Where-Object { (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0 }

if ($emptyDirs.Count -gt 0) {
    Write-Host "  Found $($emptyDirs.Count) empty directories:" -ForegroundColor Yellow
    foreach ($dir in $emptyDirs) {
        if ($PreviewOnly) {
            Write-Host "    Would remove: $($dir.Name)" -ForegroundColor Cyan
        } else {
            Remove-Item $dir.FullName -Force -ErrorAction SilentlyContinue
            Write-Host "    Removed: $($dir.Name)" -ForegroundColor Green
        }
    }
} else {
    Write-Host "  No empty directories found" -ForegroundColor Gray
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
if ($PreviewOnly) {
    Write-Host "PREVIEW MODE - No files deleted" -ForegroundColor Yellow
    Write-Host "Total space that would be freed: $([math]::Round($totalFreed,2)) GB" -ForegroundColor Cyan
    Write-Host "`nTo actually clean, run with specific flags:" -ForegroundColor Yellow
    Write-Host "  .\cleanup_programs_folder.ps1 -CleanPythonCache" -ForegroundColor Gray
    Write-Host "  .\cleanup_programs_folder.ps1 -CleanVSCode" -ForegroundColor Gray
    Write-Host "  .\cleanup_programs_folder.ps1 -CleanParadox" -ForegroundColor Gray
    Write-Host "  .\cleanup_programs_folder.ps1 -CleanPythonCache -CleanVSCode -CleanParadox" -ForegroundColor Gray
} else {
    Write-Host "Total space freed: $([math]::Round($totalFreed,2)) GB" -ForegroundColor Green
}

Write-Host "`n✅ Done!" -ForegroundColor Green

