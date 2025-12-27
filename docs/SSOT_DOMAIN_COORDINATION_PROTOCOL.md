# SSOT Domain Coordination Protocol

**Author:** Agent-2 (Architecture & Design) + Agent-1 (Integration & Core Systems)  
**Date:** 2025-12-26  
**Status:** ACTIVE - Coordination Protocol Established  
**Purpose:** Coordination protocol for SSOT domain updates and validation

<!-- SSOT Domain: documentation -->

---

## Executive Summary

This document defines the coordination protocol between Agent-2 (SSOT Domain Mapping Owner) and Agent-1 (Integration Domain Owner) for managing SSOT domain updates, validation, and consistency across the codebase.

**Coordination Scope:**
- Integration domain SSOT updates (services, integration, onboarding)
- Domain boundary definitions and validation
- SSOT domain consistency validation
- Architecture review integration

---

## Roles & Responsibilities

### Agent-2 (Architecture & Design - SSOT Domain Mapping Owner)

**Primary Responsibilities:**
- Maintain SSOT domain mapping document (`docs/SSOT_DOMAIN_MAPPING.md`)
- Validate SSOT domain consistency in architecture reviews
- Ensure SSOT compliance in design patterns
- Coordinate SSOT domain updates with Agent-1
- Define domain boundary definitions
- Validate domain boundaries in architecture reviews

**Capabilities:**
- SSOT domain mapping
- Architecture validation
- Domain boundary definition
- Design pattern validation
- Architecture review integration

### Agent-1 (Integration & Core Systems - Integration Domain Owner)

**Primary Responsibilities:**
- Integration domain SSOT updates (services, integration, onboarding domains)
- Coordinate domain boundary definitions
- Validate integration domain consistency
- Use SSOT validation tools (audit_imports.py, fix_consolidated_imports.py, validate_ssot_domains.py)
- Identify integration domain changes
- Implement integration domain updates

**Capabilities:**
- Integration patterns
- Domain coordination
- SSOT validation tools
- Integration domain expertise
- System integration patterns

---

## Coordination Workflow

### Workflow: Integration Domain Updates

```
1. Agent-1 identifies integration domain changes
   ↓
2. Agent-1 notifies Agent-2 of proposed changes
   ↓
3. Agent-2 validates domain boundaries and architecture alignment
   ↓
4. Agent-2 updates SSOT domain mapping document (if needed)
   ↓
5. Agent-1 implements integration domain updates
   ↓
6. Agent-2 validates domain consistency in architecture reviews
   ↓
7. Both agents coordinate on validation results
```

### Workflow: Domain Boundary Definitions

```
1. Agent-1 or Agent-2 identifies boundary definition need
   ↓
2. Both agents review domain boundaries together
   ↓
3. Agent-2 defines domain boundary definitions
   ↓
4. Agent-1 validates integration domain boundaries
   ↓
5. Agent-2 updates SSOT domain mapping document
   ↓
6. Both agents coordinate on boundary validation
```

### Workflow: SSOT Domain Consistency Validation

```
1. Agent-1 uses SSOT validation tools (audit_imports.py, validate_ssot_domains.py)
   ↓
2. Agent-1 identifies SSOT domain inconsistencies
   ↓
3. Agent-1 notifies Agent-2 of inconsistencies
   ↓
4. Agent-2 validates domain boundaries and architecture alignment
   ↓
5. Agent-2 provides validation feedback
   ↓
6. Agent-1 implements fixes (if needed)
   ↓
7. Agent-2 validates fixes in architecture reviews
```

---

## Coordination Checkpoints

### Regular Checkpoints

- **Weekly:** Domain consistency review
- **After Major Changes:** Domain boundary validation
- **Architecture Reviews:** SSOT domain validation integration

### Ad-Hoc Checkpoints

- **Domain Updates:** Immediate coordination when changes identified
- **Boundary Disputes:** Escalate to Agent-2 for resolution
- **Validation Issues:** Coordinate on fixes immediately

---

## Integration Domain Scope

### Agent-1 Owned Domains

1. **services** - Service layer, business logic, service implementations
   - **Examples:** `src/services/`, service classes, business logic
   - **Owner:** Integration (Agent-1)

2. **integration** - System integration, API integrations, external service connections
   - **Examples:** `src/integrations/`, API clients, external service adapters
   - **Owner:** Integration (Agent-1)

3. **onboarding** - Agent onboarding, system onboarding, initialization
   - **Examples:** Onboarding services, onboarding handlers, initialization
   - **Owner:** Integration (Agent-1)

### Coordination Points

- **Domain Boundary Definitions:** Coordinate with Agent-2
- **Domain Updates:** Notify Agent-2 before implementation
- **Validation:** Use SSOT validation tools, coordinate with Agent-2 on results

---

## SSOT Validation Tools

### Agent-1 Tools

1. **audit_imports.py** - Audit import dependencies, check for circular dependencies
2. **fix_consolidated_imports.py** - Fix broken imports, consolidate import statements
3. **validate_ssot_domains.py** - Validate SSOT domain tags, check domain consistency

### Usage Protocol

- **Before Domain Updates:** Run validation tools to identify issues
- **After Domain Updates:** Run validation tools to verify consistency
- **Coordinate Results:** Share validation results with Agent-2 for architecture review

---

## Communication Channels

### Primary Channels

- **A2A Messages:** For coordination requests and updates
- **Status.json Updates:** For progress tracking and status updates
- **Architecture Reviews:** For SSOT domain validation integration

### Response Times

- **Coordination Requests:** Within 30 minutes
- **Domain Updates:** Immediate notification
- **Validation Feedback:** Within 1 day

---

## Success Criteria

✅ **Protocol Established:**
- Coordination workflow defined
- Roles and responsibilities clear
- Communication channels established

✅ **Ongoing Coordination:**
- Regular checkpoints maintained
- Domain updates coordinated
- Validation feedback provided

✅ **Domain Consistency:**
- SSOT domain tags consistent
- Domain boundaries well-defined
- Architecture alignment maintained

---

## References

- **SSOT Domain Mapping:** `docs/SSOT_DOMAIN_MAPPING.md`
- **Agent-2 Status:** `agent_workspaces/Agent-2/status.json`
- **Agent-1 Status:** `agent_workspaces/Agent-1/status.json`

---

**Last Updated:** 2025-12-26 by Agent-2 + Agent-1  
**Next Review:** After first coordination checkpoint

