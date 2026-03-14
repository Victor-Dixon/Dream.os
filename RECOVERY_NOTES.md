<!-- SSOT Domain: documentation -->

# RECOVERY_NOTES

Recovery metadata is SSOT-managed in:

- `docs/recovery/recovery_registry.yaml`

## Re-entry verification run (2026-03-14)

Completed checks:
- `python tools/validation/check_recovery_registry.py` ✅
- `python tools/recovery_notes/check_compliance.py` ✅
- `python tools/file_header_validator.py validate` ⚠️ (repo-wide baseline drift remains)
- Discord compatibility import smoke test ⚠️ found missing `ENHANCED_BROADCAST_TEMPLATES` export; repaired in `src/discord_commander/templates/broadcast_templates.py`

## Current blockers

1. File-header protocol validator reports large baseline debt (`violation_count: 1153`) and violations on new files under `src/core/*` and `tools/recovery_notes/check_compliance.py`.
2. Duplication/incomplete-work scan still reports known duplicate groups and TODO/NotImplemented hotspots.

## Policy

- Ownership and boundary notes live only in the registry.
- File headers are pointer-only and must reference a valid registry id.
- If a core file role changes, update registry first, then code.
