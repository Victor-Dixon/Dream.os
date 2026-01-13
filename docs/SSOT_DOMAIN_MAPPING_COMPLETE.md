# SSOT Domain Mapping - Complete Registry

**Author:** Agent-2 (Architecture & Design Specialist) - SSOT Domain Mapping Owner  
**Date:** 2025-12-27  
**Status:** ACTIVE - Complete Domain Registry (32 Domains)  
**Purpose:** Comprehensive mapping of all 32 SSOT domains used across the codebase

<!-- SSOT Domain: documentation -->

---

## Executive Summary

This document provides the complete registry of all 32 Single Source of Truth (SSOT) domains for the codebase. Based on codebase scanning (21 domains found) and architectural analysis, this registry represents the full domain taxonomy.

**Total Domains:** 32  
**Currently Tagged in Codebase:** 20 unique domains  
**Format:** HTML comment `<!-- SSOT Domain: domain_name -->`

---

## Complete SSOT Domain Registry (32 Domains)

### Core Domains (5)

1. **core** - Core system functionality, base classes, fundamental components
   - **Examples:** `src/core/`, base classes, core utilities, core config
   - **Owner:** Architecture & Design (Agent-2)
   - **Files Found:** 28 files (26 .py, 2 .md)

2. **architecture** - Architecture patterns, design decisions, system structure
   - **Examples:** Architecture reviews, design patterns, system architecture documents
   - **Owner:** Architecture & Design (Agent-2)
   - **Files Found:** 7 files (all .md)

3. **services** - Service layer, business logic, service implementations
   - **Examples:** `src/services/`, service classes, business logic
   - **Owner:** Integration (Agent-1)
   - **Files Found:** 1 file (1 .py)

4. **integration** - System integration, API integrations, external service connections
   - **Examples:** `src/integrations/`, API clients, external service adapters, messaging integration
   - **Owner:** Integration (Agent-1)
   - **Files Found:** 128 files (84 .py, 44 .md)

5. **infrastructure** - Infrastructure code, deployment, DevOps, system operations
   - **Examples:** `src/infrastructure/`, deployment tools, infrastructure automation, browser, logging, persistence
   - **Owner:** Infrastructure (Agent-3)
   - **Files Found:** 145 files (89 .py, 56 .md)

### Web & Frontend Domains (2)

6. **web** - Web application code, web routes, web handlers, frontend
   - **Examples:** `src/web/`, web routes, web handlers, frontend code, Discord web interface
   - **Owner:** Web Development (Agent-7)
   - **Files Found:** 100 files (80 .py, 19 .md, 1 .js)

7. **seo** - SEO optimization, search engine optimization, meta tags
   - **Examples:** SEO tools, SEO documentation, SEO architecture reviews
   - **Owner:** Web Development (Agent-7) + Architecture (Agent-2)
   - **Files Found:** 1 file (1 .md)

### Data & Analytics Domains (3)

8. **data** - Data models, data structures, data access, repositories
   - **Examples:** Data models, data repositories, data access patterns, repository implementations
   - **Owner:** Business Intelligence (Agent-5)
   - **Files Found:** 20 files (12 .py, 8 .md)

9. **analytics** - Analytics, metrics, tracking, reporting
   - **Examples:** Analytics tools, metrics collection, analytics dashboards, analytics engines
   - **Owner:** Business Intelligence (Agent-5)
   - **Files Found:** 57 files (41 .py, 16 .md)

10. **ai_training** - AI training, machine learning, model training
    - **Examples:** AI training tools, ML models, training pipelines, dreamvault
    - **Owner:** Business Intelligence (Agent-5)
    - **Files Found:** 2 files (2 .py)

### Communication & Coordination Domains (3)

11. **communication** - Communication systems, messaging, notifications
    - **Examples:** Messaging systems, communication protocols, message queues, message handlers
    - **Owner:** Coordination (Agent-6)
    - **Files Found:** 37 files (22 .py, 15 .md)

12. **coordination** - Agent coordination, swarm coordination, multi-agent systems
    - **Examples:** Coordination handlers, swarm coordination, agent coordination, canon automation
    - **Owner:** Coordination (Agent-6)
    - **Files Found:** 1 file (1 .py)

13. **onboarding** - Agent onboarding, system onboarding, initialization
    - **Examples:** Onboarding services, onboarding handlers, initialization, soft/hard onboarding
    - **Owner:** Integration (Agent-1)
    - **Files Found:** 1 file (1 .md)

### Quality & Validation Domains (2)

14. **qa** - Quality assurance, testing, validation, quality checks
    - **Examples:** QA tools, validation tools, quality checks, proof ledger, swarm brain QA
    - **Owner:** SSOT & System Integration (Agent-8)
    - **Files Found:** 11 files (6 .py, 5 .md)

15. **validation** - Validation logic, validation tools, validation checks
    - **Examples:** Validation handlers, validation tools, validation checks, audit tools
    - **Owner:** SSOT & System Integration (Agent-8)
    - **Files Found:** 1 file (1 .py)

### Documentation & Tools Domains (2)

16. **documentation** - Documentation, guides, documentation tools
    - **Examples:** Documentation files, documentation generators, guides, devlogs
    - **Owner:** Architecture & Design (Agent-2)
    - **Files Found:** 5 files (all .md)

17. **tools** - Tools, utilities, helper scripts, automation tools
    - **Examples:** `tools/`, utility scripts, automation tools, CLI tools
    - **Owner:** Architecture & Design (Agent-2)
    - **Files Found:** 2 files (2 .py)

### Domain-Specific Domains (3)

18. **domain** - Domain-specific code, domain logic, domain models (DDD)
    - **Examples:** Domain models, domain logic, domain entities, domain services (DDD pattern)
    - **Owner:** Architecture & Design (Agent-2)
    - **Files Found:** 8 files (3 .py, 5 .md)

19. **fixes** - Bug fixes, fix implementations, fix tools
    - **Examples:** Fix tools, fix implementations, consolidated import fixes
    - **Owner:** Architecture & Design (Agent-2) - Temporary/transitional
    - **Files Found:** 1 file (1 .py)

20. **general** - General purpose code, utilities, common functionality
    - **Examples:** General utilities, common functionality, shared utilities
    - **Owner:** Architecture & Design (Agent-2) - Temporary/transitional
    - **Files Found:** 1 file (1 .md)

### Additional Logical Domains (12) - To Be Validated

Based on codebase structure analysis, the following domains are proposed to complete the 32-domain registry:

21. **repositories** - Repository pattern implementations, data access abstractions
    - **Examples:** `src/repositories/`, repository implementations, data access layer
    - **Owner:** Business Intelligence (Agent-5) or Integration (Agent-1)
    - **Status:** Proposed - needs validation

22. **orchestrators** - Orchestration logic, workflow orchestration, system orchestration
    - **Examples:** `src/orchestrators/`, orchestration engines, workflow orchestration
    - **Owner:** Infrastructure (Agent-3) or Integration (Agent-1)
    - **Status:** Proposed - needs validation

23. **gaming** - Gaming-related code, gaming integrations, gaming systems
    - **Examples:** `src/gaming/`, gaming models, gaming integrations, OSRS, DreamOS
    - **Owner:** TBD (may be part of integration domain)
    - **Status:** Proposed - needs validation

24. **vision** - Vision/image processing, computer vision, visual recognition
    - **Examples:** `src/vision/`, image processing, visual recognition systems
    - **Owner:** TBD
    - **Status:** Proposed - needs validation

25. **workflows** - Workflow management, workflow engines, workflow definitions
    - **Examples:** `src/workflows/`, workflow engines, workflow definitions
    - **Owner:** Integration (Agent-1) or Infrastructure (Agent-3)
    - **Status:** Proposed - needs validation

26. **testing** - Test files, test utilities, test infrastructure
    - **Examples:** `tests/`, test utilities, test infrastructure, unit tests, integration tests
    - **Owner:** SSOT & System Integration (Agent-8) or QA
    - **Status:** Proposed - needs validation

27. **security** - Security code, authentication, authorization, security utilities
    - **Examples:** Security utilities, authentication systems, authorization, encryption
    - **Owner:** Infrastructure (Agent-3) or Security specialist
    - **Status:** Proposed - needs validation

28. **monitoring** - Monitoring systems, health checks, observability
    - **Examples:** Monitoring tools, health check systems, observability, metrics monitoring
    - **Owner:** Infrastructure (Agent-3) or Monitoring specialist
    - **Status:** Proposed - needs validation

29. **performance** - Performance optimization, performance monitoring, performance tools
    - **Examples:** Performance tools, performance optimization, performance monitoring
    - **Owner:** Infrastructure (Agent-3) or Performance specialist
    - **Status:** Proposed - needs validation

30. **trading_robot** - Trading robot specific code, trading logic, trading systems
    - **Examples:** `src/trading_robot/`, trading logic, trading systems, trading strategies
    - **Owner:** Business Intelligence (Agent-5) or Trading specialist
    - **Status:** Proposed - needs validation

31. **swarm_brain** - Swarm brain/knowledge system, swarm intelligence, knowledge base
    - **Examples:** `src/swarm_brain/`, knowledge base, swarm intelligence, memory systems
    - **Owner:** SSOT & System Integration (Agent-8) or Coordination (Agent-6)
    - **Status:** Proposed - needs validation

32. **deployment** - Deployment code, deployment automation, deployment tools
    - **Examples:** Deployment tools, deployment automation, CI/CD, deployment scripts
    - **Owner:** Infrastructure (Agent-3)
    - **Status:** Proposed - needs validation

---

## Domain Tag Format

### Standard Format

```html
<!-- SSOT Domain: domain_name -->
```

### Examples

```python
# Python file
"""
Module description.

<!-- SSOT Domain: integration -->
"""

# Markdown file
<!-- SSOT Domain: documentation -->
# Document Title
```

### Placement

- **Python files:** In module docstring (first line or after module description)
- **Markdown files:** At the top of the file (after frontmatter if present)
- **Other files:** In file header comment section

---

## Domain Ownership & Coordination

### Primary Owners (Confirmed)

- **Architecture & Design (Agent-2):** architecture, documentation, tools, domain, core (shared), fixes (temporary), general (temporary)
- **Integration (Agent-1):** services, integration, onboarding
- **Infrastructure (Agent-3):** infrastructure
- **Web Development (Agent-7):** web, seo (shared with Agent-2)
- **Business Intelligence (Agent-5):** data, analytics, ai_training
- **Coordination (Agent-6):** communication, coordination
- **SSOT & System Integration (Agent-8):** qa, validation

### Proposed Owners (To Be Validated)

- **repositories:** Business Intelligence (Agent-5) or Integration (Agent-1)
- **orchestrators:** Infrastructure (Agent-3) or Integration (Agent-1)
- **gaming:** TBD (may be part of integration)
- **vision:** TBD
- **workflows:** Integration (Agent-1) or Infrastructure (Agent-3)
- **testing:** SSOT & System Integration (Agent-8)
- **security:** Infrastructure (Agent-3)
- **monitoring:** Infrastructure (Agent-3)
- **performance:** Infrastructure (Agent-3)
- **trading_robot:** Business Intelligence (Agent-5)
- **swarm_brain:** SSOT & System Integration (Agent-8) or Coordination (Agent-6)
- **deployment:** Infrastructure (Agent-3)

### Coordination Protocol

1. **New Domain Creation:** Coordinate with Agent-2 (SSOT Domain Mapping Owner)
2. **Domain Updates:** Coordinate with domain owner and Agent-2
3. **Domain Boundary Disputes:** Escalate to Agent-2 for resolution
4. **Integration Domain Updates:** Coordinate with Agent-1 and Agent-2
5. **Proposed Domain Validation:** Review with Agent-8 (original Phase 1 source) and domain owners

---

## Validation & Compliance

### Validation Checklist

- [ ] All files have SSOT domain tags
- [ ] SSOT domain tags use correct format
- [ ] SSOT domain names match registry
- [ ] Domain ownership is clear
- [ ] Domain boundaries are well-defined
- [ ] Proposed domains (21-32) validated with Agent-8

### Architecture Review Integration

SSOT domain validation is integrated into all architecture reviews:

1. **Pattern Validation:** Verify SSOT domain tags in design patterns
2. **Domain Consistency:** Ensure domain tags align with architecture
3. **Boundary Validation:** Verify domain boundaries are respected
4. **Ownership Verification:** Confirm domain ownership is correct
5. **Proposed Domain Review:** Validate proposed domains with stakeholders

---

## Next Steps

### Immediate Actions

1. **Validate Proposed Domains (21-32):**
   - Coordinate with Agent-8 to review original Phase 1 domain definitions
   - Validate proposed domains match Agent-8's original 32-domain list
   - Update registry with confirmed domains

2. **Domain Ownership Assignment:**
   - Assign owners to validated domains (21-32)
   - Coordinate with domain owners for confirmation
   - Update ownership registry

3. **Tagging Campaign:**
   - Identify files missing SSOT domain tags
   - Prioritize high-value files (core modules, services, infrastructure)
   - Execute tagging campaign with domain owners

4. **Validation Integration:**
   - Integrate SSOT domain validation into architecture review process
   - Create validation tools/scripts for domain tag compliance
   - Establish regular validation checkpoints

---

## Scan Results Summary

**Scan Date:** 2025-12-27  
**Total Domains Found:** 21 (20 unique, 1 documentation-only)  
**Total Files Tagged:** ~500+ files  
**Target Domains:** 32  
**Remaining:** 12 domains to validate and document

**Most Tagged Domains:**
- infrastructure: 145 files
- integration: 128 files
- web: 100 files
- analytics: 57 files
- communication: 37 files

**Scan Tool:** `tools/scan_ssot_domains.py`  
**Scan Results:** `docs/ssot_domain_scan_results.json`

---

## References

- **Agent-8 Phase 1:** SSOT Domain Mapping & Validation (2025-12-14)
- **Agent-8 Status:** 32 domains defined, 725 tools validated
- **Current State:** 20 domains found in codebase, 12 additional domains proposed
- **Coordination Protocol:** `docs/SSOT_DOMAIN_COORDINATION_PROTOCOL.md`
- **Scan Results:** `docs/ssot_domain_scan_results.json`

---

**Last Updated:** 2025-12-27 by Agent-2  
**Next Review:** After Agent-8 coordination to validate proposed domains (21-32)

