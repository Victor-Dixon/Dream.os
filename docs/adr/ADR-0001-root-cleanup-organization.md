# ADR-0001: Root Cleanup Organization

## Status
Accepted

## Context
The repository root contained a large number of cleanup and audit artifacts, which made it harder to discover the current cleanup plan and increased navigation overhead. We also need a clear SSOT location for cleanup guidance and audit outputs to support ongoing maintenance and automation.

## Decision
- Store the root cleanup plan under `docs/plans/`.
- Store cleanup audit artifacts under `reports/audits/cleanup/`.
- Store directory audit artifacts under `reports/audits/directory/`.

These locations are the SSOT for cleanup guidance and audit outputs going forward.

## Consequences
- The repository root is cleaner and more navigable.
- Cleanup guidance and audit artifacts are centralized, improving discoverability.
- Future cleanup automation can rely on stable, documented locations.
