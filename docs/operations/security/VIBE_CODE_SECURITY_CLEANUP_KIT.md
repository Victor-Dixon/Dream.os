# Vibe Code Security Cleanup — Prompt Kit v1

## Swarm Integration Notes
**Added to Agent Cellphone V2 Repository**: 2026-01-11
**Recommended for**: Agent-4 (Quality Assurance) integration
**Use Case**: Pre-deployment security audits for web applications

---

## 0) Paste-Once Input Block (REQUIRED)
Use this at the top of any audit prompt to stop "hand-wavy" answers.

APP_CONTEXT:
  stack:
    nextjs: "14.x (app router?)"
    supabase: "hosted/local"
    prisma: "yes/no"
    stripe: "yes/no"
    hosting: "vercel/other"
  auth:
    provider: "supabase auth"
    session_access: "cookies / headers / localStorage"
    admin_definition: "isAdmin flag / roles table / JWT custom claims"
  app_surface:
    public_pages: [ ... ]
    protected_pages: [ ... ]
    admin_pages: [ ... ]
    api_routes:
      - path: "/api/..."
        methods: ["GET","POST"]
        purpose: "..."
        auth: "none/jwt/cookie"
        reads_tables: ["..."]
        writes_tables: ["..."]
    server_actions: [ ... ] # if used
    edge_middleware: "yes/no"
  database:
    tables:
      - name: "users"
        owner_key: "id"
        rls: "on/off"
        policies: ["...paste..."]
      - name: "subscriptions"
        owner_key: "user_id"
        rls: "on/off"
        policies: ["...paste..."]
      - name: "payments"
      - name: "projects"
      - name: "api_keys"
    sensitive_columns:
      - "stripe_customer_id"
      - "api_key_hash"
      - "email"
      - "billing_address"
  stripe:
    products_prices: "where stored"
    webhook:
      route: "/api/stripe/webhook"
      verification: "constructEvent? yes/no"
      idempotency: "event_id stored? yes/no"
    entitlements_source_of_truth: "db/stripe"
  secrets:
    env_vars: ["..."]
    any_client_exposure_suspected: "yes/no"
  paste_code:
    - "middleware.ts"
    - "supabase client init (server + client)"
    - "1-3 riskiest API routes"
    - "stripe webhook handler"
    - "admin gating logic"
    - "RLS policies (SQL)"
    - "prisma schema (if used)"

## 1) Output Contract (MAKE THE MODEL OBEY THIS)
When you run any prompt, require this exact structure:

OUTPUT:
  ship_blockers:
    - id: "SB-001"
      severity: "CRITICAL"
      exploit: "how an attacker wins"
      affected: ["route/table/component"]
      fix: "what to change"
      patch: "code/sql snippet"
      test: "how to verify"
  this_week:
    - id: "W-001"
      severity: "HIGH|MED"
      fix + test
  roadmap:
    - "hardening + monitoring"
  verification_suite:
    - "RLS tests"
    - "API auth tests"
    - "webhook spoof tests"
  assumptions:
    - "anything you guessed"

---

## 2) Prompt: 30-Minute Lockdown (Pre-Launch)
"EMERGENCY VIBE FIX. Use the OUTPUT contract above.

Given APP_CONTEXT + paste_code:
1) Identify top 5 ship-blockers (auth bypass, data leak, payment spoof, admin takeover).
2) Provide the fastest safe patches (minimal refactor).
3) Provide a verification checklist I can run in 30 minutes.
4) Give me what to monitor in the first 24 hours post-launch."

---

## 3) Prompt: RLS Reality Check (Supabase)
"Audit my Supabase RLS like an attacker.

Do:
- For each table: who can SELECT/INSERT/UPDATE/DELETE and why.
- Flag 'USING true', 'WITH CHECK true', missing policies, and admin bypasses.
- Provide corrected policies and explain the rule in one sentence each.
- Provide test queries for:
  (a) anon user
  (b) regular user A
  (c) regular user B
  (d) admin
Use OUTPUT contract."

---

## 4) Prompt: Next.js Route Hardening Sweep
"Scan my Next.js routes (route handlers + server actions) for:
- missing authentication
- broken authorization (IDOR)
- client-trusted fields (user_id from body)
- missing input validation
- unsafe error leakage

Provide:
- a reusable authz wrapper
- zod schemas for critical inputs
- patches for the 3 worst routes
Use OUTPUT contract."

---

## 5) Prompt: Stripe Security Refactor (Keep It Simple)
"My Stripe flow is a vibe mess. Secure it without rewriting the app.

You must ensure:
- webhook signature verification
- idempotency by event_id
- entitlement checks server-side only
- no client-trusted price/product decisions
- correct handling of out-of-order events

Provide:
- minimal schema changes
- webhook handler patch
- entitlement query pattern
- tests for spoof + replay + race conditions
Use OUTPUT contract."

---

## 6) Prompt: Admin Panel Consolidation + RBAC
"Fix my admin chaos with consistent RBAC.

Must include:
- single source of truth for roles
- consistent checks in routes + pages + server actions
- audit logging for admin actions
- least privilege defaults

Provide:
- role model (tables + RLS)
- shared guard utilities
- migration steps (minimal downtime)
Use OUTPUT contract."

---

## 7) Prompt: Secrets + Client Exposure Sweep
"Find every way secrets or privileged data could leak:
- NEXT_PUBLIC misuse
- client supabase using service role key (should never happen)
- server responses returning sensitive columns
- logs leaking tokens

Provide:
- exact grep targets / file patterns
- remediation steps
- prevention rules (lint/CI checks)
Use OUTPUT contract."