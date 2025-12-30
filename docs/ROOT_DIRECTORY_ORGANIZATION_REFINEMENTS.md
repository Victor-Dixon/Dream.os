# Root Directory Organization - Documentation Strategy Refinements
**Created:** 2025-12-29  
**Author:** Agent-6 (Documentation Organization Lead)  
**Status:** ✅ Approved - Ready for Execution

## Executive Summary

Refinements to Agent-3's 5-phase migration plan, focusing on documentation structure alignment, professional presentation standards, and long-term maintainability.

## Alignment with Existing Organization Plan

**Phase 1 (Agent-6) - COMPLETE:**
- ✅ Historical audit reports archived
- ✅ Investigation reports archived
- ✅ Task log variants archived
- ✅ SSOT files consolidated
- ✅ Temporary files moved to archive/temp/

**Remaining Work (149 files identified by Agent-3):**
- 58 MD files (documentation, reports, guides)
- 16 JSON files (configs, audit results, data)
- 29 Python files (scripts, tests, tools)
- 40 other files (configs, PHP, misc)

## Documentation Organization Strategy Refinements

### 1. **MD Files Categorization Strategy**

#### **Active Documentation** → `docs/` (structured by domain)
```
docs/
  guides/          # QUICK_START_GUIDE.md, DELEGATION_BOARD.md, etc.
  standards/       # STANDARDS.md, DEPRECATION_NOTICES.md
  protocols/       # SWARM_TASK_PACKETS.md, QUEUE_PROCESSOR_USAGE.md
  architecture/    # TASK_MANAGEMENT_INTEGRATION_SUMMARY.md, etc.
  planning/        # 2026_* planning documents
  audits/          # Recent audit reports (move to archive after 90 days)
  reports/         # Recent status reports (move to archive after 90 days)
```

#### **Historical Reports** → `docs/archive/reports/` (by year/date)
- Completion reports (PHASE_0_COMPLETION_REPORT.md)
- Implementation summaries (PHASE_0_IMPLEMENTATION_SUMMARY.md)
- PR reviews (PR_REVIEW_*.md)
- Status summaries (various *_SUMMARY.md)

#### **Planning Documents** → `docs/planning/` (by year)
- 2026_DAILY_QUICK_REFERENCE.md
- 2026_EXECUTION_MANIFESTO.md
- 2026_SWARM_OS_MARKETING_AUTOMATION.md

### 2. **JSON Files Organization Strategy**

#### **Configuration Files** → `config/` (Agent-3)
- cursor_agent_coords.json
- CURSOR_MCP_CONFIG.json
- agent_mode_config.json
- config.py → Consider if this should be `config/config.py` or remain in root

#### **Audit/Report Data** → `reports/data/` (structured by type)
```
reports/
  data/
    audits/        # AGENT6_TOOL_AUDIT_RESULTS.json, toolbelt_health_audit.json
    ssot/          # ssot_validation_results.json
    v2/            # v2_violations_*.json files
    coordination/  # coordination_cache.json
```

#### **Analysis Data** → `data/analysis/`
- v2_violations_analysis.json
- v2_violations_categorized.json

### 3. **Python Scripts Organization Strategy**

#### **Standalone Tools** → `tools/standalone/` (one-off scripts)
- check_remote_posts.py
- check_site_status.py
- check_website_status.py
- investigate_fri_500.py
- fix_weareswarm_menu.py
- deploy_trp_templates.py
- setup_trp_pages.py

#### **Test Files** → `tests/standalone/` (root-level tests)
- test_atomic_file_ops.py
- test_main_integration.py
- test_onboarding_import.py
- test_php_syntax_*.py
- test_safety_components.py

#### **Audit Scripts** → `tools/audit/` (if reusable) or `scripts/audit/`
- audit_categories.py
- audit_toolbelt.py
- simple_tool_audit.py

#### **Config/Site Scripts** → `scripts/site_management/`
- configure_analytics_placeholders.py
- sync_*.py (sync_crosby_theme.py, sync_swarm_theme.py, etc.)

#### **One-Time Scripts** → `scripts/one_time/` or archive
- complete_agent8_batch1.py

### 4. **Professional Presentation Standards**

#### **README.md Enhancement**
- Add "Project Structure" section pointing to organized directories
- Update links to reflect new file locations
- Add "Navigation Guide" for finding common files

#### **Documentation Index** (`docs/DOCUMENTATION_INDEX.md`)
- Central navigation hub for all documentation
- Categorized by: Guides, Standards, Protocols, Reports, Archives
- Cross-references to related documentation

#### **Naming Conventions**
- **Reports**: `YYYY-MM-DD_descriptive_name.md` (e.g., `2025-12-29_root_directory_organization.md`)
- **Guides**: `DESCRIPTIVE_NAME_GUIDE.md` (e.g., `QUICK_START_GUIDE.md`)
- **Standards**: `STANDARD_NAME.md` (e.g., `STANDARDS.md`)
- **Configs**: `lowercase_with_underscores.json` (e.g., `cursor_agent_coords.json`)

### 5. **Archive Strategy Alignment**

#### **90-Day Rule**
- Active files in `docs/audits/`, `docs/reports/` → Move to `docs/archive/` after 90 days
- Use file modification dates to determine age
- Create automated cleanup script (future enhancement)

#### **Archive Structure**
```
docs/archive/
  audits/
    2025/           # By year
    2026/
  reports/
    2025/
    2026/
  investigations/
    2025/
    2026/
  task_logs/
```

### 6. **Integration Points with Agent-3's Plan**

**Agent-3's 5-Phase Plan Alignment:**
1. **Phase 1 (docs→docs/)**: ✅ Refined categorization strategy above
2. **Phase 2 (JSONs→data/config/reports/)**: ✅ Aligned with JSON organization strategy
3. **Phase 3 (scripts→scripts/subdirs)**: ✅ Aligned with Python scripts organization
4. **Phase 4 (temp cleanup)**: ✅ Already addressed in Phase 1
5. **Phase 5 (config consolidation)**: ✅ Aligned with config strategy

## Recommended Execution Sequence

1. **Agent-3**: Execute infrastructure reorganization per refined plan
2. **Agent-6**: Update documentation index and README.md after file moves
3. **Both**: Coordinate checkpoint after each phase for validation
4. **Agent-6**: Create navigation guide for common file locations
5. **Both**: Final validation - verify no broken links or import paths

## Professional Presentation Standards

### **Documentation Hierarchy**
```
Root
├── README.md (entry point)
├── docs/
│   ├── DOCUMENTATION_INDEX.md (central navigation)
│   ├── guides/ (how-to guides)
│   ├── standards/ (code standards, conventions)
│   ├── protocols/ (operational protocols)
│   ├── architecture/ (system architecture docs)
│   ├── planning/ (year-based planning docs)
│   └── archive/ (historical docs by year/type)
├── config/ (all configuration files)
├── reports/
│   ├── data/ (JSON data files)
│   └── ssot/ (SSOT-related reports)
└── scripts/ (organized by purpose)
```

### **Navigation Enhancement**
- All documentation cross-references related docs
- DOCUMENTATION_INDEX.md acts as master navigation hub
- README.md links to DOCUMENTATION_INDEX.md
- Each directory has README.md describing its contents (optional)

## Validation Checklist

After Agent-3 completes infrastructure reorganization:
- [ ] All MD files categorized and moved
- [ ] All JSON files organized (config vs. data)
- [ ] All Python scripts organized (tools vs. scripts vs. tests)
- [ ] README.md updated with new structure
- [ ] DOCUMENTATION_INDEX.md created/updated
- [ ] All import paths validated (Agent-3)
- [ ] No broken links in documentation
- [ ] Archive structure follows 90-day rule

## Next Steps

1. **Agent-3 Review**: Review refinements, approve or suggest changes
2. **Parallel Execution**: Agent-3 executes infrastructure org, Agent-6 updates docs
3. **Checkpoint 1**: After MD file organization
4. **Checkpoint 2**: After JSON/Python organization
5. **Checkpoint 3**: After config consolidation
6. **Final Validation**: Navigation, links, imports verified

---

**Status:** Ready for Agent-3 review and approval  
**Timeline:** Review 15-30 min, execution can begin immediately after approval

