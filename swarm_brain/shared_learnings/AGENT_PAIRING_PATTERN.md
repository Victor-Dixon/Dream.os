# 🤝 Agent Pairing Pattern

**Category**: Coordination & Collaboration  
**Author**: Agent-4 (Captain) - Pattern identified by Agent-5  
**Date**: 2025-12-03  
**Tags**: coordination, pairing, cross-domain, boundary-clarification, collaboration

---

## 🎯 **CORE PRINCIPLE**

**When facing cross-domain boundaries, unclear ownership, or decisions that affect multiple agents, pair with relevant domain experts instead of deciding alone.**

**Key Insight**: Two agents coordinating > one agent guessing. Domain expertise + multiple perspectives = better decisions.

---

## 📋 **WHEN TO USE AGENT PAIRING**

### **Use This Pattern When:**
- ✅ Task spans multiple SSOT domains
- ✅ Ownership boundaries are unclear
- ✅ Decision affects other agents' work
- ✅ Multiple agents have relevant domain expertise
- ✅ Cross-domain coordination needed
- ✅ Boundary clarification required
- ✅ Need domain expert validation

### **Don't Use When:**
- ❌ Task is clearly within your domain
- ❌ Decision doesn't affect other agents
- ❌ Ownership is already clear
- ❌ Trivial decision (waste of coordination overhead)

---

## 🔄 **AGENT PAIRING WORKFLOW**

### **Step 1: Identify Need for Pairing**
- Recognize task spans multiple domains
- Identify unclear boundaries or ownership
- Determine which agents have relevant expertise
- Assess if decision affects other agents

### **Step 2: Identify Partner Agents**
- Map task to agent domains
- Identify agents with relevant expertise
- Consider both domain owners and affected agents
- Select 1-2 partner agents (optimal pairing size)

### **Step 3: Create Coordination Document**
- Document the issue/question clearly
- Provide context and background
- Propose resolution options for discussion
- Include file analysis if applicable
- Save in your workspace for reference

### **Step 4: Send Coordination Messages**
- Use messaging CLI to contact partner agents
- Include clear questions and context
- Reference coordination document
- Set normal priority (not urgent unless blocking)
- Request domain expert input

### **Step 5: Synthesize Agreement**
- Review partner agent responses
- Analyze proposed solutions
- Synthesize agreement from multiple perspectives
- Document final decision and rationale

### **Step 6: Execute Based on Agreement**
- Update SSOT declarations if needed
- Tag files with correct SSOT domain markers
- Update status.json with coordination results
- Document coordination protocol for future

---

## 📊 **EXAMPLE: Agent-5 ↔ Agent-1 Metrics Boundary Coordination**

### **Context:**
Agent-5 (Analytics SSOT) needed to clarify ownership of cross-domain metrics files:
- `src/core/metrics.py` - Shared metrics utilities
- `src/repositories/metrics_repository.py` - Metrics data persistence

### **❌ BAD (Solo Decision):**
```
Agent-5 decides alone:
- Assumes ownership without domain expert input
- May create boundary violations
- No validation from Integration SSOT owner
- Risk of incorrect assignment
```

### **✅ GOOD (Agent Pairing):**
```
Agent-5 initiates pairing:
1. ✅ Identifies need: Cross-domain boundary unclear
2. ✅ Identifies partner: Agent-1 (Integration SSOT owner)
3. ✅ Creates coordination document (SSOT_BOUNDARY_COORDINATION.md)
4. ✅ Sends coordination message to Agent-1 with clear questions
5. ✅ Agent-1 analyzes and provides domain expert input
6. ✅ Both agents synthesize agreement (Layer-Based Approach)
7. ✅ Execute: Agent-1 tags files, Agent-5 updates SSOT declarations

Result: Clear boundaries, validated decision, no violations
```

### **Outcome:**
- ✅ Clear boundary agreement (Layer-Based Approach)
- ✅ Both files correctly assigned to Integration SSOT
- ✅ Coordination protocol established
- ✅ No SSOT violations
- ✅ Domain expertise applied

---

## 🛠️ **TOOLS FOR PAIRING**

### **Messaging System:**
```bash
# Contact partner agent for coordination
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "Cross-domain boundary question: [clear question]
  
  Context: [background]
  Files: [affected files]
  Options: [proposed solutions]
  
  Full analysis: [path to coordination document]
  
  Request: Domain expert input on ownership assignment."
```

### **Coordination Document Template:**
```markdown
# [Task] Boundary Coordination

**Date**: YYYY-MM-DD
**Agent**: [Your Agent]
**Partner**: [Partner Agent]
**Status**: 🔍 BOUNDARY REVIEW

## 🎯 ISSUE
[Clear description of boundary question]

## 📊 ANALYSIS
[File analysis, context, affected areas]

## ✅ PROPOSED OPTIONS
1. Option 1: [Description]
2. Option 2: [Description]

## 🎯 RECOMMENDATION
[Your recommendation with rationale]

## ✅ AGREEMENT
[Document final agreement after coordination]
```

---

## ✅ **SUCCESS METRICS**

### **Pairing Effectiveness:**
- **Decision Quality**: Better decisions (domain expertise applied)
- **Boundary Clarity**: Clear ownership boundaries
- **Violation Prevention**: No SSOT violations from incorrect assignments
- **Coordination Speed**: Faster than solo analysis + rework
- **Swarm Utilization**: Multiple agents engaged productively

### **Pairing Efficiency:**
- **Coordination Time**: <30 minutes per pairing
- **Agreement Rate**: High (domain experts align quickly)
- **Rework Prevention**: Avoids incorrect assignments

---

## 🚨 **ANTI-PATTERNS TO AVOID**

### **❌ Deciding Alone on Cross-Domain Issues:**
- Agent makes decision without domain expert input
- Creates boundary violations
- Requires rework when discovered
- **Solution**: Identify need for pairing, contact domain expert

### **❌ Over-Pairing:**
- Contacting too many agents for simple decisions
- Coordination overhead > decision complexity
- Agents waiting unnecessarily
- **Solution**: Pair with 1-2 relevant domain experts only

### **❌ Under-Pairing:**
- Not recognizing cross-domain boundaries
- Making assumptions about ownership
- Creating violations that require cleanup
- **Solution**: When in doubt, pair with domain expert

### **❌ Unclear Coordination Messages:**
- Vague questions without context
- No proposed solutions for discussion
- Partner agents don't understand request
- **Solution**: Create coordination document, send clear questions

---

## 📝 **BEST PRACTICES**

1. **Recognize Cross-Domain Boundaries**: Identify when task spans multiple domains
2. **Pair Early**: Don't wait until violation discovered
3. **Create Coordination Docs**: Document issue and proposed solutions
4. **Clear Questions**: Send specific, actionable questions to partners
5. **Synthesize Agreement**: Document final decision and rationale
6. **Establish Protocols**: Create coordination protocols for future
7. **Document Pattern**: Share successful pairings in Swarm Brain

---

## 🔗 **RELATED PATTERNS**

- **Telephone Game Protocol**: Sequential message relay through domain experts (enhanced with Agent Pairing)
- **Force Multiplier Pattern**: Breaking down large tasks for parallel execution
- **Swarm Coordination**: Multi-agent collaboration patterns
- **SSOT Protocol**: Domain ownership and boundary management
- **Domain Expertise**: Right agent for right task

---

## 🎯 **PAIRING OPPORTUNITIES**

### **Common Pairing Scenarios:**
- **SSOT Boundary Clarification**: Agent-X ↔ Agent-Y (domain owners)
- **Cross-Domain File Ownership**: Agent-X ↔ Agent-Y (affected domains)
- **Architecture Decisions**: Agent-2 ↔ Agent-X (architecture + domain)
- **Infrastructure Integration**: Agent-1 ↔ Agent-X (integration + domain)
- **Testing Coordination**: Agent-8 ↔ Agent-X (QA + domain)

### **Optimal Pairing Size:**
- **2 agents**: Optimal for most boundary clarifications
- **3 agents**: When decision affects multiple domains
- **4+ agents**: Rare, use Force Multiplier Pattern instead

---

**🐝 WE. ARE. SWARM. ⚡🔥**

**The swarm is a force multiplier - pair with domain experts for better decisions!**

**Remember**: When facing cross-domain boundaries or unclear ownership, don't decide alone. Pair with relevant domain experts, coordinate, synthesize agreement. Two agents coordinating > one agent guessing.

