# Final Push - Complete Secret Removal
# Execute AFTER closing Cursor/IDE
# Run as Administrator: PowerShell -ExecutionPolicy Bypass -File .\FINAL_PUSH_SECRET_REMOVAL.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Final Push - Secret Removal" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verify Cursor is closed
$cursorProcesses = Get-Process -Name "Cursor" -ErrorAction SilentlyContinue
if ($cursorProcesses) {
    Write-Host "⚠️  WARNING: Cursor is still running!" -ForegroundColor Red
    Write-Host "Please close Cursor completely before running this script." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "✅ Cursor is closed. Proceeding..." -ForegroundColor Green
Write-Host ""

# Navigate to repository
$repoPath = "D:\Agent_Cellphone_V2_Repository"
$mirrorPath = "D:\temp\Agent_Cellphone_V2_Repository.git"

if (-not (Test-Path $repoPath)) {
    Write-Host "❌ Repository path not found: $repoPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $mirrorPath)) {
    Write-Host "❌ Cleaned mirror path not found: $mirrorPath" -ForegroundColor Red
    exit 1
}

Set-Location $repoPath

Write-Host "📍 Repository: $repoPath" -ForegroundColor Cyan
Write-Host "📍 Cleaned Mirror: $mirrorPath" -ForegroundColor Cyan
Write-Host ""

# Option 1: Quick Fix - Reset Current Repository
Write-Host "🔧 Option 1: Quick Fix - Resetting current repository..." -ForegroundColor Yellow
Write-Host ""

# Remove corrupted .git if needed
if (Test-Path ".git") {
    Write-Host "Removing existing .git directory..." -ForegroundColor Yellow
    Remove-Item .git -Recurse -Force -ErrorAction SilentlyContinue
}

# Initialize fresh
Write-Host "Initializing fresh repository..." -ForegroundColor Yellow
git init

# Add remotes
Write-Host "Adding remotes..." -ForegroundColor Yellow
git remote add origin https://github.com/Dadudekc/AutoDream.Os.git -f 2>$null
git remote set-url origin https://github.com/Dadudekc/AutoDream.Os.git
git remote add cleaned-mirror $mirrorPath -f 2>$null

# Fetch cleaned history
Write-Host "Fetching cleaned history from mirror..." -ForegroundColor Yellow
git fetch cleaned-mirror

# Reset to cleaned branch
Write-Host "Resetting to cleaned branch..." -ForegroundColor Yellow
git reset --hard cleaned-mirror/agent

Write-Host ""
Write-Host "✅ Repository reset complete!" -ForegroundColor Green
Write-Host ""

# Verification
Write-Host "🔍 Verifying .env removal..." -ForegroundColor Cyan
$envInHistory = git log --all --full-history --source -- .env 2>&1
if ($envInHistory -match "fatal:" -or $envInHistory -eq "") {
    Write-Host "✅ .env not found in history - Clean!" -ForegroundColor Green
} else {
    Write-Host "⚠️  WARNING: .env still found in history!" -ForegroundColor Red
    Write-Host $envInHistory
}

Write-Host ""
Write-Host "🚀 Ready to push. Execute the following command manually:" -ForegroundColor Yellow
Write-Host "   git push origin agent --force" -ForegroundColor White
Write-Host ""
Write-Host "Or press Enter to auto-push (force push):" -ForegroundColor Yellow
$response = Read-Host
if ($response -eq "") {
    Write-Host "Pushing to origin..." -ForegroundColor Yellow
    git push origin agent --force
    Write-Host ""
    Write-Host "✅ Push complete!" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Final Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Checking latest commits on origin..." -ForegroundColor Yellow
git log origin/agent --oneline | Select-Object -First 5
Write-Host ""
Write-Host "✅ Secret removal complete!" -ForegroundColor Green


