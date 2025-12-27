$files = @(
  "websites_inventory.json",
  "websites_inventory.md",
  "websites_findings.json",
  "websites_findings.md",
  "master_task_log_web_lane.md"
)

$dir = "D:\Agent_Cellphone_V2_Repository\runtime\task_discovery"
$allExist = $true

Write-Host "Verifying artifacts..."
foreach ($f in $files) {
  $path = Join-Path $dir $f
  if (Test-Path $path) {
    $size = (Get-Item $path).Length
    Write-Host "  OK $f ($size bytes)"
  } else {
    Write-Host "  MISSING $f"
    $allExist = $false
  }
}

Write-Host ""
Write-Host "Validating JSON files..."
try {
  $inv = Get-Content (Join-Path $dir "websites_inventory.json") -Raw | ConvertFrom-Json
  Write-Host "  OK websites_inventory.json - Valid JSON, $($inv.Count) sites"
} catch {
  Write-Host "  ERROR websites_inventory.json - Invalid JSON"
  $allExist = $false
}

try {
  $findings = Get-Content (Join-Path $dir "websites_findings.json") -Raw | ConvertFrom-Json
  Write-Host "  OK websites_findings.json - Valid JSON, $($findings.Count) findings"
  
  $passCount = ($findings | Where-Object { $_.status -eq 'PASS' }).Count
  $warnCount = ($findings | Where-Object { $_.status -eq 'WARN' }).Count
  $failCount = ($findings | Where-Object { $_.status -eq 'FAIL' }).Count
  
  Write-Host "     - PASS: $passCount"
  Write-Host "     - WARN: $warnCount"
  Write-Host "     - FAIL: $failCount"
} catch {
  Write-Host "  ERROR websites_findings.json - Invalid JSON"
  $allExist = $false
}

Write-Host ""
if ($allExist) {
  Write-Host "SUCCESS All artifacts verified"
} else {
  Write-Host "FAILED Verification failed"
  exit 1
}

