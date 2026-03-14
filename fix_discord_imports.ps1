# Fix Discord Commander Import Paths
# Convert absolute imports to relative imports

Write-Host "Starting Discord Commander import fixes..."

# Get all Python files in discord_commander directory
$discordFiles = Get-ChildItem -Path "src/discord_commander" -Recurse -Filter "*.py" -File

Write-Host "Found $($discordFiles.Count) Python files in discord_commander"

$changesMade = 0

foreach ($file in $discordFiles) {
    Write-Host "Processing: $($file.FullName)"
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    $fileChanged = $false

    # Fix imports based on directory depth
    $relativePath = $file.DirectoryName.Replace("$PSScriptRoot\src\", "").Replace("\", "/")
    $depth = ($relativePath -split "/").Count
    Write-Host "  Relative path: $relativePath, Depth: $depth"

    # Keep absolute imports but fix incorrect ones
    # Pattern 1: Fix incorrect messaging_infrastructure import
    $oldContent = $content
    $content = $content -replace 'from src\.services\.messaging_infrastructure import ConsolidatedMessagingService', 'from src.services.messaging.service_adapters import ConsolidatedMessagingService'
    if ($content -ne $oldContent) { Write-Host "  Fixed ConsolidatedMessagingService import" }

    # Pattern 2: Fix incorrect messaging_models_core import
    $content = $content -replace 'from src\.core\.messaging_models_core import MessageCategory', 'from src.core.messaging_models_core import MessageCategory'
    if ($content -ne $oldContent) { Write-Host "  Fixed MessageCategory import" }

    # Pattern 3: Fix specific known incorrect imports
    $oldContent = $content
    $content = $content -replace 'from src\.services\.messaging_infrastructure import ConsolidatedMessagingService', 'from ...services.messaging.service_adapters import ConsolidatedMessagingService'
    if ($content -ne $oldContent) { Write-Host "  Fixed ConsolidatedMessagingService import" }

    # Pattern 4: Fix discord_commander internal imports (should be relative)
    $oldContent = $content
    $content = $content -replace 'from src\.discord_commander\.([^;\n]+)', 'from ..$1'
    if ($content -ne $oldContent) { Write-Host "  Fixed discord_commander internal import" }

    # Check if file was changed
    if ($content -ne $originalContent) {
        $content | Set-Content $file.FullName -Encoding UTF8
        Write-Host "  ✅ Fixed imports in: $($file.FullName)"
        $changesMade++
        $fileChanged = $true
    } else {
        Write-Host "  No changes needed"
    }
    Write-Host ""
}

Write-Host "Import fixes completed. Modified $changesMade files."

# Test a few files to make sure imports work
Write-Host "Testing import fixes..."
try {
    & python -c "import sys; sys.path.insert(0, 'src'); from discord_commander.views.agent_messaging_view import AgentMessagingView; print('✅ agent_messaging_view imports fixed')"
} catch {
    Write-Host "❌ agent_messaging_view still has import issues: $($_.Exception.Message)"
}

try {
    & python -c "import sys; sys.path.insert(0, 'src'); from discord_commander.controllers.broadcast_controller_view import BroadcastControllerView; print('✅ broadcast_controller_view imports fixed')"
} catch {
    Write-Host "❌ broadcast_controller_view still has import issues: $($_.Exception.Message)"
}

Write-Host "Import fix verification completed."