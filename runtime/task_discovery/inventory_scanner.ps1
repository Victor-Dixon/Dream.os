$Root = "D:\websites"
$OutDir = "D:\Agent_Cellphone_V2_Repository\runtime\task_discovery"

function Get-SiteType($p) {
  if (Test-Path (Join-Path $p "wp-config.php")) { return "wordpress" }
  if (Test-Path (Join-Path $p "package.json")) {
    try {
      $pkg = Get-Content (Join-Path $p "package.json") -Raw | ConvertFrom-Json
      $deps = @()
      if ($pkg.dependencies) { $deps += $pkg.dependencies.PSObject.Properties.Name }
      if ($pkg.devDependencies) { $deps += $pkg.devDependencies.PSObject.Properties.Name }
      if ($deps -contains "next") { return "nextjs" }
      if ($deps -contains "vite") { return "vite" }
      if ($deps -contains "@astrojs/core") { return "astro" }
      if ($deps -contains "react-scripts") { return "cra" }
      return "node"
    } catch {
      return "node"
    }
  }
  if (Test-Path (Join-Path $p "index.html")) { return "static" }
  return "unknown"
}

function Get-Entrypoints($p, $type) {
  $eps = @()
  switch ($type) {
    "wordpress" { $eps += "wp-config.php"; break }
    "nextjs" { 
      if (Test-Path (Join-Path $p "next.config.js")) { $eps += "next.config.js" }
      $eps += "package.json"
      break 
    }
    "vite" { $eps += "vite.config.*"; $eps += "package.json"; break }
    "astro" { $eps += "astro.config.*"; $eps += "package.json"; break }
    "cra" { $eps += "package.json"; break }
    "node" { $eps += "package.json"; break }
    "static" { $eps += "index.html"; break }
    default { }
  }
  return ($eps | ForEach-Object { $_.ToString() }) -join ", "
}

Write-Host "Scanning $Root for site roots..."

$roots = Get-ChildItem -Path $Root -Directory -Recurse -ErrorAction SilentlyContinue |
  Where-Object {
    (Test-Path (Join-Path $_.FullName "wp-config.php")) -or
    (Test-Path (Join-Path $_.FullName "package.json")) -or
    (Test-Path (Join-Path $_.FullName "index.html"))
  } |
  Select-Object -Unique FullName

Write-Host "Found $($roots.Count) potential site roots. Processing..."

$inventory = @()

foreach ($r in $roots) {
  $type = Get-SiteType $r.FullName
  $entry = Get-Entrypoints $r.FullName $type

  $pkgScripts = $null
  if (Test-Path (Join-Path $r.FullName "package.json")) {
    try {
      $pkg = Get-Content (Join-Path $r.FullName "package.json") -Raw | ConvertFrom-Json
      if ($pkg.scripts) { 
        $pkgScripts = ($pkg.scripts.PSObject.Properties | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join "; " 
      }
    } catch { 
      $pkgScripts = "package.json parse failed" 
    }
  }

  $inventory += [pscustomobject]@{
    name       = Split-Path $r.FullName -Leaf
    path       = $r.FullName
    type       = $type
    entrypoints= $entry
    scripts    = $pkgScripts
  }
  
  Write-Host "  - Found: $($inventory[-1].name) ($type)"
}

# Save JSON inventory
$inventory | ConvertTo-Json -Depth 6 | Out-File (Join-Path $OutDir "websites_inventory.json") -Encoding utf8

# Save Markdown inventory
$md = @()
$md += "# Websites Inventory ($Root)"
$md += ""
$md += "| Name | Type | Entrypoints | Path |"
$md += "|---|---|---|---|"
foreach ($i in $inventory) {
  $md += "| $($i.name) | $($i.type) | $($i.entrypoints) | $($i.path) |"
}
$md -join "`n" | Out-File (Join-Path $OutDir "websites_inventory.md") -Encoding utf8

Write-Host ""
Write-Host "✅ Inventory scan complete: $($inventory.Count) sites discovered"
Write-Host "✅ Generated websites_inventory.json and websites_inventory.md"

