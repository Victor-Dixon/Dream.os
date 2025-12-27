# SSOT Domain Mapping

**Author:** Agent-2 (Architecture & Design Specialist) - SSOT Domain Mapping Owner  
**Date:** 2025-12-26  
**Status:** ACTIVE - Maintained by Agent-2  
**Purpose:** Comprehensive mapping of all SSOT domains used across the codebase

<!-- SSOT Domain: documentation -->

---

## Executive Summary

This document provides a comprehensive mapping of all Single Source of Truth (SSOT) domains used across the codebase. SSOT domains are used to categorize and organize code, tools, and documentation to ensure clear ownership and maintainability.

**Total Domains:** 32 (as defined by Agent-8 Phase 1)  
**Currently Tagged in Codebase:** 20 unique domains found  
**Proposed Additional Domains:** 12 domains (to be validated with Agent-8)  
**Format:** HTML comment `<!-- SSOT Domain: domain_name -->`  
**Scan Date:** 2025-12-27  
**Scan Tool:** `tools/scan_ssot_domains.py`  
**Scan Results:** `docs/ssot_domain_scan_results.json`

---

## SSOT Domain Registry

### Core Domains

1. **core** - Core system functionality, base classes, fundamental components
   - **Examples:** `src/core/`, base classes, core utilities
   - **Owner:** Architecture & Design

2. **architecture** - Architecture patterns, design decisions, system structure
   - **Examples:** Architecture reviews, design patterns, system architecture
   - **Owner:** Architecture & Design (Agent-2)

3. **services** - Service layer, business logic, service implementations
   - **Examples:** `src/services/`, service classes, business logic
   - **Owner:** Integration (Agent-1)

4. **integration** - System integration, API integrations, external service connections
   - **Examples:** `src/integrations/`, API clients, external service adapters
   - **Owner:** Integration (Agent-1)

5. **infrastructure** - Infrastructure code, deployment, DevOps, system operations
   - **Examples:** `src/infrastructure/`, deployment tools, infrastructure automation
   - **Owner:** Infrastructure (Agent-3)

### Web & Frontend Domains

6. **web** - Web application code, web routes, web handlers, frontend
   - **Examples:** `src/web/`, web routes, web handlers, frontend code
   - **Owner:** Web Development (Agent-7)

7. **seo** - SEO optimization, search engine optimization, meta tags
   - **Examples:** SEO tools, SEO documentation, SEO architecture reviews
   - **Owner:** Web Development (Agent-7) + Architecture (Agent-2)

### Data & Analytics Domains

8. **data** - Data models, data structures, data access
   - **Examples:** Data models, data repositories, data access patterns
   - **Owner:** Business Intelligence (Agent-5)

9. **analytics** - Analytics, metrics, tracking, reporting
   - **Examples:** Analytics tools, metrics collection, analytics dashboards
   - **Owner:** Business Intelligence (Agent-5)

### Communication & Coordination Domains

10. **communication** - Communication systems, messaging, notifications
    - **Examples:** Messaging systems, communication protocols
    - **Owner:** Coordination (Agent-6)

11. **coordination** - Agent coordination, swarm coordination, multi-agent systems
    - **Examples:** Coordination handlers, swarm coordination, agent coordination
    - **Owner:** Coordination (Agent-6)

12. **onboarding** - Agent onboarding, system onboarding, initialization
    - **Examples:** Onboarding services, onboarding handlers, initialization
    - **Owner:** Integration (Agent-1)

### Quality & Validation Domains

13. **qa** - Quality assurance, testing, validation, quality checks
    - **Examples:** QA tools, validation tools, quality checks
    - **Owner:** SSOT & System Integration (Agent-8)

14. **validation** - Validation logic, validation tools, validation checks
    - **Examples:** Validation handlers, validation tools, validation checks
    - **Owner:** SSOT & System Integration (Agent-8)

### Documentation & Tools Domains

15. **documentation** - Documentation, guides, documentation tools
    - **Examples:** Documentation files, documentation generators, guides
    - **Owner:** Architecture & Design (Agent-2)

16. **tools** - Tools, utilities, helper scripts, automation tools
    - **Examples:** `tools/`, utility scripts, automation tools
    - **Owner:** Architecture & Design (Agent-2)

### Domain-Specific Domains

17. **domain** - Domain-specific code, domain logic, domain models
    - **Examples:** Domain models, domain logic, domain-specific implementations
    - **Owner:** Architecture & Design (Agent-2)

18. **ai_training** - AI training, machine learning, model training
    - **Examples:** AI training tools, ML models, training pipelines
    - **Owner:** Business Intelligence (Agent-5)

### Additional Domains (To Be Validated)

19. **fixes** - Bug fixes, fix implementations, fix tools
    - **Examples:** Fix tools, fix implementations
    - **Owner:** TBD

20. **general** - General purpose code, utilities, common functionality
    - **Examples:** General utilities, common functionality
    - **Owner:** TBD

### Additional Domains (Proposed - To Be Validated with Agent-8)

Based on codebase structure analysis, the following 12 domains are proposed to complete the 32-domain registry. These need validation against Agent-8's original Phase 1 mapping:

21. **repositories** - Repository pattern implementations, data access abstractions  
    - **Owner:** Business Intelligence (Agent-5) or Integration (Agent-1) - TBD  
    - **Status:** Proposed - needs validation

22. **orchestrators** - Orchestration logic, workflow orchestration  
    - **Owner:** Infrastructure (Agent-3) or Integration (Agent-1) - TBD  
    - **Status:** Proposed - needs validation

23. **gaming** - Gaming-related code, gaming integrations  
    - **Owner:** TBD (may be part of integration domain)  
    - **Status:** Proposed - needs validation

24. **vision** - Vision/image processing, computer vision  
    - **Owner:** TBD  
    - **Status:** Proposed - needs validation

25. **workflows** - Workflow management, workflow engines  
    - **Owner:** Integration (Agent-1) or Infrastructure (Agent-3) - TBD  
    - **Status:** Proposed - needs validation

26. **testing** - Test files, test utilities, test infrastructure  
    - **Owner:** SSOT & System Integration (Agent-8) - Proposed  
    - **Status:** Proposed - needs validation

27. **security** - Security code, authentication, authorization  
    - **Owner:** Infrastructure (Agent-3) - Proposed  
    - **Status:** Proposed - needs validation

28. **monitoring** - Monitoring systems, health checks, observability  
    - **Owner:** Infrastructure (Agent-3) - Proposed  
    - **Status:** Proposed - needs validation

29. **performance** - Performance optimization, performance monitoring  
    - **Owner:** Infrastructure (Agent-3) - Proposed  
    - **Status:** Proposed - needs validation

30. **trading_robot** - Trading robot specific code, trading logic  
    - **Owner:** Business Intelligence (Agent-5) - Proposed  
    - **Status:** Proposed - needs validation

31. **swarm_brain** - Swarm brain/knowledge system, swarm intelligence  
    - **Owner:** SSOT & System Integration (Agent-8) or Coordination (Agent-6) - TBD  
    - **Status:** Proposed - needs validation

32. **deployment** - Deployment code, deployment automation, CI/CD  
    - **Owner:** Infrastructure (Agent-3) - Proposed  
    - **Status:** Proposed - needs validation

**Note:** See `docs/SSOT_DOMAIN_MAPPING_COMPLETE.md` for full detailed registry including proposed domains.

---

## SSOT Tag Format

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

### Primary Owners

- **Architecture & Design (Agent-2):** architecture, documentation, tools, domain, core (shared)
- **Integration (Agent-1):** services, integration, onboarding
- **Infrastructure (Agent-3):** infrastructure
- **Web Development (Agent-7):** web, seo (shared with Agent-2)
- **Business Intelligence (Agent-5):** data, analytics, ai_training
- **Coordination (Agent-6):** communication, coordination
- **SSOT & System Integration (Agent-8):** qa, validation

### Coordination Protocol

1. **New Domain Creation:** Coordinate with Agent-2 (SSOT Domain Mapping Owner)
2. **Domain Updates:** Coordinate with domain owner and Agent-2
3. **Domain Boundary Disputes:** Escalate to Agent-2 for resolution
4. **Integration Domain Updates:** Coordinate with Agent-1 and Agent-2

---

## Validation & Compliance

### Validation Checklist

- [ ] All files have SSOT domain tags
- [ ] SSOT domain tags use correct format
- [ ] SSOT domain names match registry
- [ ] Domain ownership is clear
- [ ] Domain boundaries are well-defined

### Architecture Review Integration

SSOT domain validation is integrated into all architecture reviews:

1. **Pattern Validation:** Verify SSOT domain tags in design patterns
2. **Domain Consistency:** Ensure domain tags align with architecture
3. **Boundary Validation:** Verify domain boundaries are respected
4. **Ownership Verification:** Confirm domain ownership is correct

---

## Maintenance

### Responsibilities

- **Agent-2 (SSOT Domain Mapping Owner):**
  - Maintain SSOT domain mapping document
  - Validate SSOT domain consistency in architecture reviews
  - Ensure SSOT compliance in design patterns
  - Coordinate SSOT domain updates with Agent-1

### Update Protocol

1. **New Domain:** Add to registry with owner and examples
2. **Domain Update:** Update registry and notify domain owner
3. **Domain Removal:** Archive domain and update registry
4. **Ownership Change:** Update registry and coordinate with both owners

---

## References

- **Agent-8 Phase 1:** SSOT Domain Mapping & Validation (2025-12-14)
- **Agent-8 Status:** 32 domains defined, 725 tools validated
- **Current State:** 20 domains found in codebase, 12 additional domains to be documented

---

**Last Updated:** 2025-12-27 by Agent-2  
**Next Review:** Coordinate with Agent-8 to validate proposed domains (21-32) and complete 32-domain registry  
**Complete Registry:** See `docs/SSOT_DOMAIN_MAPPING_COMPLETE.md` for full detailed registry with all 32 domains

