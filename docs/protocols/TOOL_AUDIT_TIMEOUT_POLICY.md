- Classify `timeout` during quick tool scans as **SLOW**, not broken.
- Broken = syntax/import/runtime errors on import OR non-timeout execution errors.
- For `tools/*` package modules, execute with `python -m tools.<path>` to avoid relative-import failures.
- Keep `--help` fast: no network calls, no long imports, no side effects.
- Record scan output as evidence when claiming Phase 3 “broken tools” progress.

