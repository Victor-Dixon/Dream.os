<!-- SSOT Domain: documentation -->

# RECOVERY_NOTES

Recovery metadata is now SSOT-managed in:

- `docs/recovery/recovery_registry.yaml`

## Usage
1. Read the registry entries for the active core files.
2. Use `main.py` as the runtime entrypoint.
3. Run `python tools/validation/check_recovery_registry.py` after boundary changes.

## Policy
- Ownership and boundary notes live only in the registry.
- File headers are pointer-only and must reference a valid registry id.
- If a core file role changes, update registry first, then code.
