$OutDir = "D:\Agent_Cellphone_V2_Repository\runtime\task_discovery"
$inv = Get-Content (Join-Path $OutDir "websites_inventory.json") -Raw | ConvertFrom-Json
$findings = @()

Write-Host "Running health checks on $($inv.Count) sites..."

foreach ($s in $inv) {
  $status = "PASS"
  $notes = @()

  Write-Host "  Checking: $($s.name) ($($s.type))"

  if ($s.type -in @("nextjs","vite","astro","cra","node")) {
    if (-not (Test-Path (Join-Path $s.path "node_modules"))) {
      $status = "WARN"
      $notes += "node_modules missing (needs install)"
    }
    if ($s.scripts -and ($s.scripts -match "build=")) {
      $notes += "has build script"
    } else {
      $status = "WARN"
      $notes += "no build script detected"
    }
  }

  if ($s.type -eq "wordpress") {
    $notes += "WP root detected; check themes/plugins versions separately"
  }

  if ($s.type -eq "static") {
    # Check for basic HTML structure
    $indexPath = Join-Path $s.path "index.html"
    if (Test-Path $indexPath) {
      $content = Get-Content $indexPath -Raw -ErrorAction SilentlyContinue
      if ($content) {
        if ($content -notmatch "<title>") {
          $status = "WARN"
          $notes += "missing <title> tag"
        }
        if ($content -notmatch "<meta.*description") {
          $status = "WARN"
          $notes += "missing meta description"
        }
        if ($content -match "<title>.*</title>") {
          $notes += "has title tag"
        }
      } else {
        $status = "FAIL"
        $notes += "index.html is empty"
      }
    } else {
      $status = "FAIL"
      $notes += "index.html not found"
    }
  }

  if ($notes.Count -eq 0) {
    $notes += "no issues detected"
  }

  $findings += [pscustomobject]@{
    name = $s.name
    type = $s.type
    path = $s.path
    status = $status
    notes = ($notes -join " | ")
  }
}

# Save JSON findings
$findings | ConvertTo-Json -Depth 6 | Out-File (Join-Path $OutDir "websites_findings.json") -Encoding utf8

# Save Markdown findings
$md = @()
$md += "# Websites Findings"
$md += ""
$md += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$md += ""
$md += "| Name | Type | Status | Notes |"
$md += "|---|---|---|---|"
foreach ($f in $findings) {
  $md += "| $($f.name) | $($f.type) | $($f.status) | $($f.notes) |"
}
$md += ""
$md += "## Summary"
$md += ""
$md += "- Total sites: $($findings.Count)"
$md += "- PASS: $(($findings | Where-Object { $_.status -eq 'PASS' }).Count)"
$md += "- WARN: $(($findings | Where-Object { $_.status -eq 'WARN' }).Count)"
$md += "- FAIL: $(($findings | Where-Object { $_.status -eq 'FAIL' }).Count)"

$md -join "`n" | Out-File (Join-Path $OutDir "websites_findings.md") -Encoding utf8

Write-Host ""
Write-Host "✅ Health checks complete"
Write-Host "   - PASS: $(($findings | Where-Object { $_.status -eq 'PASS' }).Count)"
Write-Host "   - WARN: $(($findings | Where-Object { $_.status -eq 'WARN' }).Count)"
Write-Host "   - FAIL: $(($findings | Where-Object { $_.status -eq 'FAIL' }).Count)"
Write-Host "✅ Generated websites_findings.json and websites_findings.md"

