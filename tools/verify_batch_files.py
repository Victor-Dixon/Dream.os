"""Verify batch file line counts."""
from pathlib import Path

project_root = Path(__file__).parent.parent

files_to_check = {
    'Batch 1': {
        'base_monitoring_manager.py': Path('src/core/managers/monitoring/base_monitoring_manager.py'),
        'base_manager.py': Path('src/core/managers/base_manager.py'),
        'core_configuration_manager.py': Path('src/core/managers/core_configuration_manager.py'),
    },
    'Batch 2': {
        'unified_discord_bot.py': Path('src/discord_commander/unified_discord_bot.py'),
    },
    'Batch 3': {
        'vector_integration_unified.py': Path('src/services/vector_integration_unified.py'),
        'vector_database_service_unified.py': Path('src/services/vector_database_service_unified.py'),
    },
    'Batch 4': {
        'unified_onboarding_service.py': Path('src/services/unified_onboarding_service.py'),
    },
}

print("=" * 80)
print("BATCH FILE VERIFICATION")
print("=" * 80)

for batch, files in files_to_check.items():
    print(f"\n{batch}:")
    for name, filepath in files.items():
        full_path = project_root / filepath
        if full_path.exists():
            line_count = len(full_path.read_text(encoding='utf-8').splitlines())
            status = "✅ COMPLIANT" if line_count <= 400 else "⚠️ VIOLATION"
            print(f"  {name}: {line_count} lines {status}")
        else:
            print(f"  {name}: NOT FOUND")
