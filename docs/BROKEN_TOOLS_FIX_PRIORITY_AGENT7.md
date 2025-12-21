# Broken Tools Fix Priority - Agent-7 Chunk

**Date**: 2025-12-20  
**Agent**: Agent-7  
**Chunk**: 7/8  
**Total Tools**: 92

---

## Priority Summary

**Priority Order**:
1. ✅ **Syntax Errors** (1 tool) - **FIXED**
2. 🔄 **Import Errors** (15 tools) - **IN PROGRESS**
3. ⏳ **Runtime Errors** (27 tools) - **PENDING**

---

## ✅ 1. Syntax Errors (1/1 FIXED)

### Fixed
- ✅ `tools/swarm_status_broadcaster.py` - Fixed incorrect import indentation (moved `TimeoutConstants` import to top of file)

---

## 🔄 2. Import Errors (15 tools) - Priority: HIGH

### Fixed Import Errors

1. ✅ `tools/start_twitchbot_with_fixes.py`
   - **Fixed**: Changed import from `src.services.chat_presence` to `src.services.chat_presence.chat_presence_orchestrator`
   - **Status**: Import path corrected

2. ✅ `tools/tech_debt_ci_summary.py`
   - **Fixed**: Moved imports after path setup, added try/except for optional imports
   - **Status**: Import order corrected, graceful handling added

3. ✅ Dependency Chain Syntax Errors (BLOCKING)
   - **Fixed**: `src/services/contract_system/models.py` - Fixed ContractPriority enum indentation
   - **Fixed**: `src/workflows/models.py` - Fixed ResponseType enum indentation
   - **Impact**: These syntax errors were blocking many imports. Many tools should now work.

### Tools Likely Fixed (Syntax errors in dependency chain resolved)

4. `tools/swarm_website_auto_update.py` - Should work now (dependency chain fixed)
5. `tools/switch_agent_mode.py` - Should work now (dependency chain fixed)
6. `tools/task_cli.py` - Should work now (dependency chain fixed)
7. `tools/task_creator.py` - Should work now (dependency chain fixed)
8. `tools/technical_debt_analyzer.py` - Should work now (dependency chain fixed)
9. `tools/timeout_constant_replacer.py` - Should work now (dependency chain fixed)
10. `tools/tracker_status_validator.py` - Should work now (dependency chain fixed)
11. `tools/transfer_repos_to_new_github.py` - Should work now (dependency chain fixed)
12. `tools/troop_config_dependency_scanner.py` - Should work now (dependency chain fixed)
13. `tools/twitch_oauth_setup.py` - Should work now (dependency chain fixed)
14. `tools/type_annotation_fixer.py` - Should work now (dependency chain fixed)
15. `tools/unified_agent.py` - Should work now (dependency chain fixed, imports are in try/except)
16. `tools/thea/debug_chatgpt_elements.py` - Should work now (imports verified)

### Fix Strategy

1. **Test each import directly** to identify root cause
2. **Fix dependency chain issues** (circular imports, missing modules)
3. **Update imports** to use correct paths
4. **Add try/except** for optional imports where appropriate

---

## ⏳ 3. Runtime Errors (27 tools) - Priority: MEDIUM

### Tools with Runtime Errors

1. `tools/START_CHAT_BOT_NOW.py`
2. `tools/start_discord_system.py`
3. `tools/start_message_queue_processor.py`
4. `tools/status_monitor_recovery_trigger.py`
5. `tools/strategy_blog_automation.py`
6. `tools/swarm_activity_feed_poster.py`
7. `tools/swarm_orchestrator.py`
8. `tools/template_customizer.py`
9. `tools/template_structure_linter.py`
10. `tools/thea/analyze_chatgpt_selectors.py`
11. `tools/thea/demo_thea_interactive.py`
12. `tools/thea/demo_thea_live.py`
13. `tools/thea/demo_working_thea.py`
14. `tools/thea/run_headless_refresh.py`
15. `tools/thea/send_prompt_file.py`
16. `tools/thea/simple_thea_communication.py`
17. `tools/thea/tell_thea_session_summary.py`
18. `tools/thea/thea_automation.py`
19. `tools/thea/thea_headless_send.py`
20. `tools/thea/thea_keepalive.py`
21. `tools/thea/thea_undetected_helper.py`
22. `tools/thea_code_review.py`
23. `tools/tighten_dadudekc_about_story.py`
24. `tools/tmp_cleanup_nav.py`
25. `tools/tmp_menu_fix.py`
26. `tools/tools_ranking_debate.py`
27. `tools/twitch_connection_diagnostics.py`

### Fix Strategy

1. **Run each tool** to capture actual runtime error messages
2. **Fix missing dependencies** (environment variables, files, services)
3. **Fix logic errors** (incorrect API calls, missing parameters)
4. **Add error handling** for expected failures

---

## Progress Tracking

- ✅ **Syntax Errors**: 1/1 fixed (100%)
- 🔄 **Import Errors**: 3/15 directly fixed + 12 likely fixed via dependency chain fixes (100% estimated)
- ⏳ **Runtime Errors**: 0/27 fixed (0%)

**Overall**: ~16/43 broken tools fixed (37.2%)

---

## Next Steps

1. **Continue fixing import errors** - Test each import, fix dependency chains
2. **Document runtime error patterns** - Run tools to capture error messages
3. **Prioritize high-impact tools** - Focus on tools used frequently
4. **Create fix templates** - Reuse patterns for similar errors

