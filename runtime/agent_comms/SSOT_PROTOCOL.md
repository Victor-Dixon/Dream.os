# 🔗 SSOT GROUP PROTOCOL

**Version**: 1.0  
**Date**: 2025-01-27  
**Status**: ✅ **ACTIVE - GROUP PROTOCOL**  
**Priority**: CRITICAL

---

## 🎯 **PROTOCOL OVERVIEW**

SSOT (Single Source of Truth) is now a **GROUP PROTOCOL**, not a single-agent responsibility. Each agent maintains SSOT in their own domain, with Captain coordinating cross-domain enforcement.

---

## 📋 **SSOT DOMAIN OWNERSHIP**

| **Agent** | **SSOT Domain** | **Responsibilities** |
|-----------|----------------|---------------------|
| **Agent-1** | Integration SSOT | Core systems, messaging, integration patterns, execution pipelines |
| **Agent-2** | Architecture SSOT | Design patterns, architectural decisions, PR management, refactoring |
| **Agent-3** | Infrastructure SSOT | DevOps, deployment, infrastructure configs, CI/CD, validation |
| **Agent-5** | Analytics SSOT | Metrics, analytics, BI systems, reporting, technical debt tracking |
| **Agent-6** | Communication SSOT | Messaging protocols, coordination systems, swarm status |
| **Agent-7** | Web SSOT | Web frameworks, frontend/backend patterns, Discord integration |
| **Agent-8** | QA SSOT | Test infrastructure, quality standards, test coverage enforcement |
| **Agent-4** | Strategic SSOT | Coordinates SSOT enforcement, resolves conflicts, audits |

---

## 🔄 **SSOT ENFORCEMENT RULES**

### **Rule 1: Domain Ownership**
- Each agent is responsible for maintaining SSOT in their domain
- When creating new code, check for existing SSOT in your domain first
- If duplicate exists in your domain, consolidate before creating new

### **Rule 2: Cross-Domain Violations**
- If you find SSOT violation in another agent's domain, notify that agent
- If violation spans multiple domains, escalate to Captain (Agent-4)
- Captain coordinates resolution across domains

### **Rule 3: SSOT Tags**
All SSOT files must be tagged with domain:
```markdown
<!-- SSOT Domain: [agent-domain] -->
<!-- Example: SSOT Domain: integration -->
```

### **Rule 4: Change Review**
- Before modifying SSOT files, check if change affects other domains
- If cross-domain impact, coordinate with affected agents
- Captain reviews all cross-domain SSOT changes

### **Rule 5: Captain Audit Cycle**
- Captain coordinates periodic SSOT audits (weekly)
- Each agent audits their domain during audit cycle
- Violations reported to Captain for coordination

---

## 🛠️ **SSOT TOOLS & SUPPORT**

### **Agent-8 Provides:**
- SSOT violation detection tools
- SSOT validation scripts
- Consolidation utilities
- SSOT documentation

### **Agent-8 Does NOT:**
- Enforce SSOT across all 8 agents alone
- Audit all domains (only provides tools)
- Resolve violations (domain owners resolve)

---

## 📊 **SSOT VIOLATION RESOLUTION**

### **Step 1: Detection**
- Agent detects violation in their domain
- OR: Another agent detects and notifies domain owner
- OR: Captain detects during audit

### **Step 2: Assessment**
- Domain owner assesses violation severity
- Determines if consolidation needed
- Checks cross-domain impact

### **Step 3: Resolution**
- **Single Domain**: Domain owner resolves
- **Cross-Domain**: Captain coordinates resolution
- **High Priority**: Captain may assign to domain owner with deadline

### **Step 4: Validation**
- Domain owner validates resolution
- Captain verifies cross-domain changes
- SSOT tools confirm no new violations

---

## 🎯 **SSOT DECLARATION**

Each agent declares their SSOT zone in their status.json:

```json
{
  "ssot_domain": {
    "domain": "integration",
    "scope": ["core systems", "messaging", "integration patterns"],
    "ssot_files": [
      "src/core/messaging_core.py",
      "src/services/unified_messaging_service.py"
    ],
    "last_audit": "2025-01-27"
  }
}
```

---

## ✅ **SUCCESS METRICS**

### **Individual Agent:**
- Zero SSOT violations in their domain
- All domain files properly tagged
- Regular domain audits completed

### **Swarm-Wide:**
- Duplication growth rate decreases
- SSOT violations resolved faster (distributed effort)
- Captain coordination effective
- SSOT tools support group protocol

---

## 🚨 **ESCALATION**

### **When to Escalate to Captain:**
1. Cross-domain SSOT violation
2. High-priority violation requiring immediate attention
3. Disagreement on SSOT location
4. Violation affecting multiple agents

### **Captain Actions:**
1. Coordinates resolution across domains
2. Assigns tasks with deadlines if needed
3. Resolves conflicts between agents
4. Conducts periodic audits

---

## 📝 **PROTOCOL UPDATES**

This protocol is maintained by Captain (Agent-4). Updates require:
- Captain approval
- Swarm-wide notification
- Documentation update

---

**🐝 WE. ARE. SWARM. ⚡🔥**

**SSOT is now a shared responsibility - each agent owns their domain, Captain coordinates the whole.**

