# C: Drive Cleanup Script
# Safe cleanup operations for Windows C: drive

Write-Host "=== C: Drive Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Starting cleanup operations...`n" -ForegroundColor Yellow

$totalFreed = 0

# 1. Clean Temp folders (SAFE)
Write-Host "[1/6] Cleaning Temp folders..." -ForegroundColor Yellow
$tempDirs = @(
    "$env:TEMP",
    "$env:LOCALAPPDATA\Temp",
    "C:\Windows\Temp"
)

foreach ($dir in $tempDirs) {
    if (Test-Path $dir) {
        try {
            $before = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
            $after = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $freed = ($before - $after) / 1GB
            $totalFreed += $freed
            Write-Host "  Freed $([math]::Round($freed,2)) GB from $dir" -ForegroundColor Green
        } catch {
            Write-Host "  Warning: Could not fully clean $dir" -ForegroundColor Yellow
        }
    }
}

# 2. Clean npm cache (SAFE)
Write-Host "`n[2/6] Cleaning npm cache..." -ForegroundColor Yellow
if (Get-Command npm -ErrorAction SilentlyContinue) {
    try {
        $npmCache = "$env:LOCALAPPDATA\npm-cache"
        if (Test-Path $npmCache) {
            $before = (Get-ChildItem $npmCache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
            npm cache clean --force 2>&1 | Out-Null
            $after = (Get-ChildItem $npmCache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
            $freed = $before - $after
            $totalFreed += $freed
            Write-Host "  Freed $([math]::Round($freed,2)) GB from npm cache" -ForegroundColor Green
        }
    } catch {
        Write-Host "  npm cache clean failed" -ForegroundColor Yellow
    }
}

# 3. Clean Python cache (SAFE - from workspace)
Write-Host "`n[3/6] Cleaning Python __pycache__ directories..." -ForegroundColor Yellow
$workspacePath = "D:\Agent_Cellphone_V2_Repository"
if (Test-Path $workspacePath) {
    try {
        $pycacheDirs = Get-ChildItem -Path $workspacePath -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue
        $before = ($pycacheDirs | Get-ChildItem -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
        $pycacheDirs | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
        Write-Host "  Freed $([math]::Round($before,2)) MB from Python cache" -ForegroundColor Green
    } catch {
        Write-Host "  Python cache clean failed" -ForegroundColor Yellow
    }
}

# 4. Clean Windows Update cache (SAFE)
Write-Host "`n[4/6] Cleaning Windows Update cache..." -ForegroundColor Yellow
try {
    Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
    $updateCache = "C:\Windows\SoftwareDistribution\Download"
    if (Test-Path $updateCache) {
        $before = (Get-ChildItem $updateCache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        Get-ChildItem $updateCache -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
        $after = (Get-ChildItem $updateCache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $freed = $before - $after
        $totalFreed += $freed
        Write-Host "  Freed $([math]::Round($freed,2)) GB from Windows Update cache" -ForegroundColor Green
    }
    Start-Service -Name wuauserv -ErrorAction SilentlyContinue
} catch {
    Write-Host "  Windows Update cache clean failed (may need admin)" -ForegroundColor Yellow
}

# 5. Clean Recycle Bin (SAFE)
Write-Host "`n[5/6] Cleaning Recycle Bin..." -ForegroundColor Yellow
try {
    $shell = New-Object -ComObject Shell.Application
    $recycleBin = $shell.NameSpace(0xA)
    $before = ($recycleBin.Items() | Measure-Object -Property Size -Sum).Sum / 1GB
    $recycleBin.InvokeVerb("delete")
    Write-Host "  Recycle Bin cleaned" -ForegroundColor Green
} catch {
    Write-Host "  Recycle Bin clean failed" -ForegroundColor Yellow
}

# 6. Run Windows Disk Cleanup (SAFE)
Write-Host "`n[6/6] Running Windows Disk Cleanup utility..." -ForegroundColor Yellow
Write-Host "  Note: This opens the Disk Cleanup GUI - you can select additional items" -ForegroundColor Cyan
try {
    Start-Process cleanmgr.exe -ArgumentList "/d C:" -ErrorAction SilentlyContinue
} catch {
    Write-Host "  Could not launch Disk Cleanup" -ForegroundColor Yellow
}

# Summary
Write-Host "`n=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Total space freed: $([math]::Round($totalFreed,2)) GB" -ForegroundColor Green
Write-Host "`n⚠️  MANUAL CLEANUP RECOMMENDED:" -ForegroundColor Yellow
Write-Host "1. PerfectMemory folder: $env:LOCALAPPDATA\PerfectMemory (20.55 GB)" -ForegroundColor Red
Write-Host "   - Review and delete old/unused data" -ForegroundColor Gray
Write-Host "2. Programs folder: $env:LOCALAPPDATA\Programs (14.83 GB)" -ForegroundColor Red
Write-Host "   - Review and uninstall unused programs" -ForegroundColor Gray
Write-Host "3. Roblox: $env:LOCALAPPDATA\Roblox (3.25 GB)" -ForegroundColor Yellow
Write-Host "   - Delete if not needed" -ForegroundColor Gray

Write-Host "`n✅ Cleanup complete!" -ForegroundColor Green

