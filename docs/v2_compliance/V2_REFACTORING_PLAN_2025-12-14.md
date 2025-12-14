# V2 Compliance Refactoring Plan - 2025-12-14

**Author**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-12-14  
**Status**: ACTIVE PLAN

---

## 🎯 EXECUTIVE SUMMARY

**Current Status**: 1,941 violations (16.9% compliance)  
**Target**: 90%+ compliance within 6 months  
**Priority**: File size violations (113 files) first

---

## 📊 VIOLATION BREAKDOWN

### **Total Violations**: 1,941

- **File Size**: 113 files (>300 lines) - **HIGHEST PRIORITY**
- **SSOT Tags**: 737 files (missing tags) - **MEDIUM PRIORITY**
- **Function Size**: 940 functions (>30 lines) - **MEDIUM PRIORITY**
- **Class Size**: 151 classes (>200 lines) - **LOWER PRIORITY**

---

## 🚨 PHASE 1: FILE SIZE VIOLATIONS (113 files)

### **Priority Tiers**:

#### **Tier 1: Critical (>1000 lines)** - 4 files
1. `unified_discord_bot.py` - 2,636 lines (exceeds by 2,336)
2. `messaging_template_texts.py` - 1,419 lines (exceeds by 1,119)
3. `enhanced_agent_activity_detector.py` - 1,367 lines (exceeds by 1,067)
4. `github_book_viewer.py` - 1,164 lines (exceeds by 864)

**Strategy**: Break into multiple modules (5-10 files each)  
**Estimated Effort**: 2-3 weeks per file  
**Total Effort**: 8-12 weeks

#### **Tier 2: High Priority (700-1000 lines)** - 6 files
5. `thea_browser_service.py` - 1,013 lines (exceeds by 713)
6. `twitch_bridge.py` - 954 lines (exceeds by 654)
7. `main_control_panel_view.py` - 877 lines (exceeds by 577)
8. `hard_onboarding_service.py` - 870 lines (exceeds by 570)
9. `status_change_monitor.py` - 826 lines (exceeds by 526)
10. `broadcast_templates.py` - 819 lines (exceeds by 519)

**Strategy**: Extract handlers/helpers/utilities  
**Estimated Effort**: 1-2 weeks per file  
**Total Effort**: 6-12 weeks

#### **Tier 3: Medium Priority (500-700 lines)** - 10 files
11. `hardened_activity_detector.py` - 809 lines
12. `messaging_pyautogui.py` - 801 lines
13. `message_queue_processor.py` - 773 lines
14. `agent_self_healing_system.py` - 751 lines
15. `chat_presence_orchestrator.py` - 749 lines
16. `auto_gas_pipeline_system.py` - 687 lines
17. `swarm_showcase_commands.py` - 650 lines
18. `debate_to_gas_integration.py` - 619 lines
19. `message_queue.py` - 617 lines
20. `discord_gui_modals.py` - 600 lines

**Strategy**: Extract sub-modules and utilities  
**Estimated Effort**: 3-5 days per file  
**Total Effort**: 6-10 weeks

#### **Tier 4: Lower Priority (300-500 lines)** - 93 files
**Strategy**: Extract functions/classes to separate modules  
**Estimated Effort**: 1-3 days per file  
**Total Effort**: 12-18 weeks

---

## 📅 TIMELINE

### **Month 1-2: Critical Files (Tier 1)**
- Week 1-3: `unified_discord_bot.py`
- Week 4-6: `messaging_template_texts.py`
- Week 7-9: `enhanced_agent_activity_detector.py`
- Week 10-12: `github_book_viewer.py`

**Target**: 4 files → 0 violations  
**Compliance Improvement**: 16.9% → 20%

### **Month 3-4: High Priority (Tier 2)**
- 6 files refactored
- Extract handlers/helpers/utilities pattern

**Target**: 10 files → 0 violations  
**Compliance Improvement**: 20% → 25%

### **Month 5-6: Medium Priority (Tier 3)**
- 10 files refactored
- Extract sub-modules pattern

**Target**: 20 files → 0 violations  
**Compliance Improvement**: 25% → 35%

### **Month 7-12: Lower Priority (Tier 4) + SSOT Tags**
- 93 files refactored
- 737 SSOT tags added
- Function/class size violations addressed

**Target**: 113 files → 0 violations  
**Compliance Improvement**: 35% → 90%+

---

## 🛠️ REFACTORING PATTERNS

### **Pattern 1: Handler + Helper Modules**
- Extract handlers to `handlers/` directory
- Extract helpers to `helpers/` directory
- Keep main service <300 lines

### **Pattern 2: Service + Integration Modules**
- Split service logic from integration code
- Create separate integration modules
- Maintain clear boundaries

### **Pattern 3: Manager + Component Modules**
- Extract components to separate modules
- Keep manager as orchestrator
- Each component <300 lines

### **Pattern 4: Template Extraction**
- Extract templates to separate files
- Use template loading system
- Keep main file <300 lines

---

## 📋 PRIORITIZED FILE LIST

### **By Directory**:

#### **src/discord_commander/** (12 violations)
1. `unified_discord_bot.py` - 2,636 lines (Tier 1)
2. `github_book_viewer.py` - 1,164 lines (Tier 1)
3. `main_control_panel_view.py` - 877 lines (Tier 2)
4. `status_change_monitor.py` - 826 lines (Tier 2)
5. `swarm_showcase_commands.py` - 650 lines (Tier 3)
6. `discord_gui_modals.py` - 600 lines (Tier 3)
7. `discord_service.py` - 389 lines (Tier 4)
8. `messaging_commands.py` - 425 lines (Tier 4)
9. `discord_embeds.py` - 340 lines (Tier 4)
10. `status_reader.py` - 309 lines (Tier 4)
11. `systems_inventory_commands.py` - 353 lines (Tier 4)
12. `intelligence.py` - 339 lines (Tier 4)

#### **src/core/** (25 violations)
1. `messaging_template_texts.py` - 1,419 lines (Tier 1)
2. `hardened_activity_detector.py` - 809 lines (Tier 3)
3. `messaging_pyautogui.py` - 801 lines (Tier 3)
4. `message_queue_processor.py` - 773 lines (Tier 3)
5. `agent_self_healing_system.py` - 751 lines (Tier 3)
6. `auto_gas_pipeline_system.py` - 687 lines (Tier 3)
7. `debate_to_gas_integration.py` - 619 lines (Tier 3)
8. `message_queue.py` - 617 lines (Tier 3)
9. + 17 more files (Tier 4)

#### **src/services/** (7 violations)
1. `hard_onboarding_service.py` - 870 lines (Tier 2)
2. `chat_presence_orchestrator.py` - 749 lines (Tier 3)
3. + 5 more files (Tier 4)

#### **src/orchestrators/overnight/** (6 violations)
1. `enhanced_agent_activity_detector.py` - 1,367 lines (Tier 1)
2. + 5 more files (Tier 4)

#### **src/infrastructure/browser/** (3 violations)
1. `thea_browser_service.py` - 1,013 lines (Tier 2)
2. + 2 more files (Tier 4)

#### **src/services/chat_presence/** (1 violation)
1. `twitch_bridge.py` - 954 lines (Tier 2)

---

## 🎯 SUCCESS METRICS

### **Short-term (Month 1-2)**:
- ✅ 4 critical files refactored
- ✅ Compliance: 16.9% → 20%
- ✅ 0 files >1000 lines

### **Medium-term (Month 3-6)**:
- ✅ 20 files refactored
- ✅ Compliance: 20% → 35%
- ✅ 0 files >700 lines

### **Long-term (Month 7-12)**:
- ✅ 113 files refactored
- ✅ Compliance: 35% → 90%+
- ✅ 0 file size violations

---

## 📝 NEXT ACTIONS

1. **Immediate**: Update dashboard with accurate numbers
2. **Week 1**: Start Tier 1 file refactoring (`unified_discord_bot.py`)
3. **Week 2-4**: Continue Tier 1 files
4. **Month 2**: Begin Tier 2 files
5. **Ongoing**: Add SSOT tags as files are refactored

---

**Status**: ✅ **Plan Created**  
**Next**: Begin Tier 1 refactoring

🐝 **WE. ARE. SWARM. ⚡**

