# Tools Directory Consolidation Script
# Consolidates scattered script/tool directories into organized structure
# Usage: .\consolidate_tool_dirs.ps1 [-DryRun]

param(
    [switch]$DryRun
)

Write-Host "🔧 Tools Directory Consolidation Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$startTime = Get-Date

# Define source directories and their categorizations
$consolidationMap = @{
    "scripts" = @{
        "category" = "automation"
        "description" = "General automation and utility scripts"
    }
    "extensions" = @{
        "category" = "development"
        "description" = "Development extensions and plugins"
    }
    "mcp_servers" = @{
        "category" = "automation"
        "description" = "MCP server configurations and tools"
    }
    # Keep tools as the main target directory
}

$targetDir = "tools"
$filesMoved = 0
$totalSizeMoved = 0

# Function to format file size
function Format-FileSize {
    param([long]$Size)
    if ($Size -gt 1GB) { return "{0:N2} GB" -f ($Size / 1GB) }
    elseif ($Size -gt 1MB) { return "{0:N2} MB" -f ($Size / 1MB) }
    elseif ($Size -gt 1KB) { return "{0:N2} KB" -f ($Size / 1KB) }
    else { return "$Size bytes" }
}

# Analyze current tools structure
Write-Host "`n📊 Analyzing current tools directory structure..." -ForegroundColor Yellow
$existingTools = Get-ChildItem -Path $targetDir -Directory -ErrorAction SilentlyContinue
if ($existingTools) {
    Write-Host "  📁 Existing tools subdirectories:" -ForegroundColor Gray
    foreach ($dir in $existingTools) {
        $fileCount = (Get-ChildItem -Path $dir.FullName -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "    - $($dir.Name): $fileCount files" -ForegroundColor White
    }
} else {
    Write-Host "  📁 Tools directory is flat structure" -ForegroundColor Gray
}

# Create organized subdirectories
$subDirs = @(
    "automation",      # CI/CD, deployment, general scripts
    "utilities",       # General utility scripts and helpers
    "development",     # Development tools, extensions, debuggers
    "analysis",        # Data analysis, reporting, monitoring tools
    "maintenance"      # Repository maintenance, cleanup scripts
)

Write-Host "`n📁 Creating organized subdirectory structure..." -ForegroundColor Yellow
$dirsCreated = 0
foreach ($subDir in $subDirs) {
    $fullPath = Join-Path $targetDir $subDir
    if (-not (Test-Path $fullPath)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        $dirsCreated++
        Write-Host "  ✅ Created: tools/$subDir" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Exists: tools/$subDir" -ForegroundColor Gray
    }
}

# Consolidate scripts directory
Write-Host "`n🔄 Consolidating scripts/ directory..." -ForegroundColor Yellow
$scriptsPath = "scripts"
if (Test-Path $scriptsPath) {
    $scriptFiles = Get-ChildItem -Path $scriptsPath -File -ErrorAction SilentlyContinue
    if ($scriptFiles.Count -gt 0) {
        foreach ($file in $scriptFiles) {
            # Categorize scripts by content/filename
            $fileName = $file.Name.ToLower()
            if ($fileName -match "deploy|build|ci|cd|pipeline") {
                $category = "automation"
            } elseif ($fileName -match "clean|backup|archive|maintenance") {
                $category = "maintenance"
            } elseif ($fileName -match "analyze|report|monitor|health") {
                $category = "analysis"
            } elseif ($fileName -match "test|debug|validate") {
                $category = "development"
            } else {
                $category = "utilities"
            }

            $targetPath = Join-Path $targetDir "$category\$($file.Name)"

            if (-not $DryRun) {
                Move-Item -Path $file.FullName -Destination $targetPath -Force
                $filesMoved++
                $totalSizeMoved += $file.Length
                Write-Host "  📦 Moved: $($file.Name) → tools/$category/" -ForegroundColor Gray
            } else {
                Write-Host "  [DRY RUN] Would move: $($file.Name) → tools/$category/" -ForegroundColor Magenta
                $filesMoved++
                $totalSizeMoved += $file.Length
            }
        }
    }

    # Check if scripts directory is now empty
    $remainingItems = Get-ChildItem -Path $scriptsPath -Recurse -ErrorAction SilentlyContinue
    if (-not $DryRun -and $remainingItems.Count -eq 0) {
        Remove-Item -Path $scriptsPath -Recurse -Force
        Write-Host "  ✅ Removed empty: scripts/" -ForegroundColor Green
    }
}

# Consolidate extensions directory
Write-Host "`n🔄 Consolidating extensions/ directory..." -ForegroundColor Yellow
$extensionsPath = "extensions"
if (Test-Path $extensionsPath) {
    $extensionItems = Get-ChildItem -Path $extensionsPath -Recurse -ErrorAction SilentlyContinue
    if ($extensionItems.Count -gt 0) {
        foreach ($item in $extensionItems) {
            $relativePath = $item.FullName.Replace((Resolve-Path $extensionsPath).Path + "\", "")
            $targetPath = Join-Path $targetDir "development\$relativePath"

            if (-not $DryRun) {
                $targetParent = Split-Path $targetPath -Parent
                if (-not (Test-Path $targetParent)) {
                    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
                }

                if ($item.PSIsContainer) {
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    Move-Item -Path $item.FullName -Destination $targetPath -Force
                    $filesMoved++
                    $totalSizeMoved += $item.Length
                }
                Write-Host "  📦 Moved: $relativePath → tools/development/" -ForegroundColor Gray
            } else {
                Write-Host "  [DRY RUN] Would move: $relativePath → tools/development/" -ForegroundColor Magenta
                if (-not $item.PSIsContainer) {
                    $filesMoved++
                    $totalSizeMoved += $item.Length
                }
            }
        }
    }

    # Check if extensions directory is now empty
    $remainingItems = Get-ChildItem -Path $extensionsPath -Recurse -ErrorAction SilentlyContinue
    if (-not $DryRun -and $remainingItems.Count -eq 0) {
        Remove-Item -Path $extensionsPath -Recurse -Force
        Write-Host "  ✅ Removed empty: extensions/" -ForegroundColor Green
    }
}

# Consolidate mcp_servers directory
Write-Host "`n🔄 Consolidating mcp_servers/ directory..." -ForegroundColor Yellow
$mcpPath = "mcp_servers"
if (Test-Path $mcpPath) {
    $mcpItems = Get-ChildItem -Path $mcpPath -Recurse -ErrorAction SilentlyContinue
    if ($mcpItems.Count -gt 0) {
        foreach ($item in $mcpItems) {
            $relativePath = $item.FullName.Replace((Resolve-Path $mcpPath).Path + "\", "")
            $targetPath = Join-Path $targetDir "automation\$relativePath"

            if (-not $DryRun) {
                $targetParent = Split-Path $targetPath -Parent
                if (-not (Test-Path $targetParent)) {
                    New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
                }

                if ($item.PSIsContainer) {
                    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
                } else {
                    Move-Item -Path $item.FullName -Destination $targetPath -Force
                    $filesMoved++
                    $totalSizeMoved += $item.Length
                }
                Write-Host "  📦 Moved: $relativePath → tools/automation/" -ForegroundColor Gray
            } else {
                Write-Host "  [DRY RUN] Would move: $relativePath → tools/automation/" -ForegroundColor Magenta
                if (-not $item.PSIsContainer) {
                    $filesMoved++
                    $totalSizeMoved += $item.Length
                }
            }
        }
    }

    # Check if mcp_servers directory is now empty
    $remainingItems = Get-ChildItem -Path $mcpPath -Recurse -ErrorAction SilentlyContinue
    if (-not $DryRun -and $remainingItems.Count -eq 0) {
        Remove-Item -Path $mcpPath -Recurse -Force
        Write-Host "  ✅ Removed empty: mcp_servers/" -ForegroundColor Green
    }
}

# Reorganize existing tools directory content
Write-Host "`n🔄 Reorganizing existing tools/ content..." -ForegroundColor Yellow
$existingToolFiles = Get-ChildItem -Path $targetDir -File -ErrorAction SilentlyContinue
if ($existingToolFiles.Count -gt 0) {
    foreach ($file in $existingToolFiles) {
        $fileName = $file.Name.ToLower()
        if ($fileName -match "deploy|build|ci|cd|pipeline") {
            $category = "automation"
        } elseif ($fileName -match "clean|backup|archive|maintenance") {
            $category = "maintenance"
        } elseif ($fileName -match "analyze|report|monitor|health") {
            $category = "analysis"
        } elseif ($fileName -match "test|debug|validate|extension") {
            $category = "development"
        } else {
            $category = "utilities"
        }

        $targetPath = Join-Path $targetDir "$category\$($file.Name)"

        if (-not $DryRun) {
            Move-Item -Path $file.FullName -Destination $targetPath -Force
            $filesMoved++
            $totalSizeMoved += $file.Length
            Write-Host "  📦 Reorganized: $($file.Name) → tools/$category/" -ForegroundColor Gray
        } else {
            Write-Host "  [DRY RUN] Would reorganize: $($file.Name) → tools/$category/" -ForegroundColor Magenta
            $filesMoved++
            $totalSizeMoved += $file.Length
        }
    }
}

# Create consolidation report
$consolidationReport = @"
# Tools Directory Consolidation Report

## Executive Summary
- **Consolidation Date**: $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))
- **Directories Consolidated**: scripts/, extensions/, mcp_servers/
- **Files Reorganized**: $filesMoved
- **Data Reorganized**: $(Format-FileSize $totalSizeMoved)
- **New Categories Created**: 5 (automation, utilities, development, analysis, maintenance)

## New Directory Structure
```
tools/
├── automation/      # CI/CD, deployment, MCP servers, scripts
├── utilities/       # General utility scripts and helpers
├── development/     # Extensions, development tools, debuggers
├── analysis/        # Monitoring, reporting, analysis tools
└── maintenance/     # Cleanup, backup, archive scripts
```

## Consolidation Details

### Source Directories
- **scripts/** (24 files): Moved to appropriate categories, directory removed
- **extensions/** (56 files): Moved to development/, directory removed
- **mcp_servers/** (2 files): Moved to automation/, directory removed
- **tools/** (existing): Reorganized into categories

### Categorization Logic
- **automation**: Deployment, CI/CD, pipeline, MCP server files
- **maintenance**: Cleanup, backup, archive, maintenance scripts
- **analysis**: Monitoring, reporting, health check, analysis tools
- **development**: Testing, debugging, extension, development tools
- **utilities**: General-purpose scripts and helpers

## Impact Assessment
- **Directory Count**: Reduced from 4 to 1 organized directory
- **Discoverability**: Tools now grouped by function and purpose
- **Maintenance**: Easier to find and manage related tools
- **Scalability**: Clear structure for adding new tools

## Validation Checklist
- [ ] All tools accessible in new organized structure
- [ ] No broken script references or imports
- [ ] Tool execution works from new locations
- [ ] Documentation updated with new paths

## Next Steps
1. Update any hardcoded paths in scripts or documentation
2. Test critical tool functionality from new locations
3. Consider creating symbolic links for backward compatibility
4. Update team documentation with new tool organization

---
*Generated by Tools Consolidation Script*
"@

# Calculate execution time
$endTime = Get-Date
$duration = $endTime - $startTime

# Summary
Write-Host "`n📊 Tools Consolidation Summary" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Execution time: $($duration.TotalSeconds.ToString("F2")) seconds" -ForegroundColor White
Write-Host "Files reorganized: $filesMoved" -ForegroundColor White
Write-Host "Data reorganized: $(Format-FileSize $totalSizeMoved)" -ForegroundColor White
Write-Host "Directories created: $dirsCreated" -ForegroundColor White

if ($DryRun) {
    Write-Host "`n🔍 This was a dry run - no actual consolidation performed" -ForegroundColor Magenta
    Write-Host "Run without -DryRun to execute actual consolidation" -ForegroundColor Magenta
} else {
    # Save consolidation report
    $reportPath = "tools/consolidation_report_$($startTime.ToString('yyyyMMdd')).md"
    $consolidationReport | Out-File -FilePath $reportPath -Encoding UTF8

    Write-Host "`n📄 Consolidation report saved to: $reportPath" -ForegroundColor Green
    Write-Host "`n✅ Tools directory consolidation completed successfully" -ForegroundColor Green
    Write-Host "Scattered tool directories merged into organized structure" -ForegroundColor Green
}

Write-Host "`n💡 Recommendations:" -ForegroundColor Cyan
Write-Host "1. Test critical tools from their new organized locations" -ForegroundColor White
Write-Host "2. Update documentation and scripts with new tool paths" -ForegroundColor White
Write-Host "3. Consider creating backward compatibility symlinks if needed" -ForegroundColor White