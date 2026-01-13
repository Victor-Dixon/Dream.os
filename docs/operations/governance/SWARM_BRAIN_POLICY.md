# Swarm Brain Policy - NON-CANONICAL Status

## Status: NON-CANONICAL (Advisory Only)

**Swarm Brain is NOT LAW. It is MEMORY (advisory documentation only).**

## Policy Statement

Swarm Brain serves as a **knowledge repository** and **pattern library** for the Agent Cellphone V2 project. All content in Swarm Brain is **advisory** and **non-binding**. Agents may reference patterns, solutions, and learnings from Swarm Brain, but are **not required** to follow them.

## Enforcement Boundaries

### ✅ What Swarm Brain IS
- Knowledge repository for patterns and solutions
- Learning history and decision log
- Reference material for agents
- Advisory guidance for similar problems

### ❌ What Swarm Brain IS NOT
- Enforceable requirements (LAW)
- Mandatory protocols
- Required standards
- Binding contracts

## Entry Pathways

All Swarm Brain entry pathways MUST include a clear NON-CANONICAL disclaimer header. This ensures agents understand the advisory nature of the content.

### Required Disclaimer Header

```markdown
---
NON-CANONICAL: This content is advisory only and does not constitute enforceable requirements.
See docs/governance/GOVERNANCE_MAP.md for LAW vs MEMORY distinction.
---
```

## Implementation

### MCP Server
- `mcp_servers/swarm_brain_server.py` - Prepend disclaimer when `content=` parameter is missing the header

### Update Tools
- `tools/update_swarm_brain_agent*.py` - Validate and prefix disclaimer (belt-and-suspenders approach)

### Templates
- All Swarm Brain templates and prompts must include disclaimer language
- Remove any "MANDATORY" language referring to Swarm Brain requirements
- Replace with advisory language and links to governance map/policy

## Migration from "Mandatory" Language

### Before (INCORRECT)
- "Swarm Brain is MANDATORY"
- "You MUST follow Swarm Brain patterns"
- "Swarm Brain requirements"

### After (CORRECT)
- "You MAY reference Swarm Brain for patterns"
- "Swarm Brain provides advisory guidance"
- "Consider Swarm Brain learnings (non-canonical)"

## References

- Governance Map: `docs/governance/GOVERNANCE_MAP.md`
- LAW Artifacts: `.cursor/rules/*.mdc`
- Swarm Brain MCP: `mcp_servers/swarm_brain_server.py`

