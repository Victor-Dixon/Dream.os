# Tool Wishlist - 2025-12-08 (Agent-2)

## Desired Tool
**Name:** WordPress Deployment Verifier  
**Problem:** Manual WordPress/SFTP deploys are error-prone (CSS not applied until push, cache issues). Need automated preflight + postflight verification without full WP admin access.  

## Capabilities
- Validate credentials/connectivity (SFTP/WP-CLI/REST) before deploy.
- Upload a file manifest atomically with size/hash verification.
- Trigger cache flush (WP-CLI, REST, rewrite flush fallback) and verify cache clear via header checks.
- Post-deploy checks:
  - Confirm CSS/JS assets 200 OK, correct sizes/hashes.
  - Detect missing asset references (404s) on key pages.
  - Optional visual diff on top 3 pages (screenshot compare).
- Rollback helper: restore backed-up files on failure.

## Inputs/Outputs
- **Input:** Site host, creds (env/secret), manifest (local→remote paths), optional health URLs.
- **Output:** JSON report (upload results, hash matches, cache flush status, asset check results, rollback status).

## Why It Matters
- Reduces manual deployment risk for FreeRideInvestor/Prismblossom and future WP sites.
- Shortens validation cycle and catches cache/asset issues before stakeholders see regressions.

