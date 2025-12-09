# Tool I Wish I Had - 2025-12-07

## Name
`pr-auth-fallback-orchestrator`

## What it would do
- Detect gh auth failures automatically and prompt for minimal-scope token regeneration (repo, workflow) with clear scopes and expiry guidance.
- If CLI auth still fails, guide a browser-based manual PR creation flow (pre-fill titles/descriptions, attach diff summaries, and open target repos).
- Logs outcomes back to trackers (Batch 2 / Case Variations) and updates Swarm Brain devlogs automatically.

## Why
PR creation is blocked by GH CLI auth; the bottleneck is repetitive token troubleshooting and manual PR prep. This tool would cut blocker time and keep tracking artifacts in sync.

