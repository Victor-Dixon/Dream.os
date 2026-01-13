# Governance Map - Agent Cellphone V2

## Purpose

This document maps the governance structure of the Agent Cellphone V2 project, clearly distinguishing between **LAW** (enforceable requirements) and **MEMORY** (advisory documentation).

## LAW vs MEMORY

### LAW (Enforceable Requirements)
- **Source**: `.cursor/rules/*.mdc` files with `alwaysApply: true` or scoped `globs`
- **Enforcement**: Cursor IDE automatically applies these rules during development
- **Format**: MDC (Markdown with frontmatter)
- **Updates**: Changes require explicit review and approval
- **Validation**: Automated via tools and CI/CD

### MEMORY (Advisory Documentation)
- **Source**: Swarm Brain (MCP server), `docs/` directory, legacy archives
- **Enforcement**: Advisory only - agents may reference but are not required to follow
- **Format**: Various (Markdown, JSON, knowledge graph)
- **Updates**: Can be updated freely without governance review
- **Validation**: None - purely informational

## LAW Artifacts

### Core Rules (Always Applied)
- `.cursor/rules/architecture.mdc` - Core V2 architecture conventions
- `.cursor/rules/code-style.mdc` - Consistent code style standards
- `.cursor/rules/workflow.mdc` - Git workflow and collaboration standards
- `.cursor/rules/swarm-protocol.mdc` - Agent Swarm communication protocols
- `.cursor/rules/session-closure.mdc` - A+++ Session closure standard
- `.cursor/rules/v2-compliance.mdc` - V2 compliance guardrails

### Scoped Rules
- `.cursor/rules/messaging-contracts.mdc` - Messaging system contracts (scoped to `src/services/messaging/**` and `agent_workspaces/**/inbox/**`)
- `.cursor/rules/messaging/cli-flags.mdc` - CLI flag validation (scoped to messaging CLI)
- `.cursor/rules/messaging/pyautogui-operations.mdc` - PyAutoGUI delivery operations (scoped to messaging delivery)
- `.cursor/rules/git-hygiene.mdc` - Git hygiene requirements (always applied)
- `.cursor/rules/agent-workspaces.mdc` - Agent workspace management
- `.cursor/rules/documentation.mdc` - Documentation standards

### Enforcement Tools
- `tools/validate_closure_format.py` - Validates session closures against A+++ standard
- `src/services/onboarding/soft/canonical_closure_prompt.py` - Canonical closure prompt generator
- `templates/session-closure-template.md` - Template for session closures

## MEMORY Artifacts

### Swarm Brain
- **Status**: NON-CANONICAL (advisory only)
- **Access**: Via MCP server (`mcp_servers/swarm_brain_server.py`)
- **Policy**: See `docs/governance/SWARM_BRAIN_POLICY.md`
- **Usage**: Agents may search and reference, but are not required to follow patterns found there

### Documentation
- `docs/` directory - Project documentation, guides, protocols
- Legacy content - `docs/legacy/` - Deprecated documentation preserved for reference

### Deprecated Content
- `docs/legacy/code-of-conduct.md` - Former "Swarm Code of Conduct" (DEPRECATED)
- See deprecation notices in files for migration paths

## Precedence

1. **LAW (MDC rules)** - Highest priority, always enforced
2. **MEMORY (Swarm Brain/Docs)** - Advisory only, may inform decisions but do not override LAW

## References

- Swarm Brain Policy: `docs/governance/SWARM_BRAIN_POLICY.md`
- Rule Index: `.cursor/rules/README.md`
- Session Closure Standard: `.cursor/rules/session-closure.mdc`
- Validation Tool: `tools/validate_closure_format.py`

