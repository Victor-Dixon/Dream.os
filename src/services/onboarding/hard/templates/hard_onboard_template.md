<!-- SSOT Domain: onboarding -->

[HARD ONBOARDING] S2A ACTIVATION DIRECTIVE — COMPLETE SYSTEM RESET
================================================================

**Signal Type:** System → Agent (S2A)
**Priority:** Critical
**Mode:** Hard Reset Protocol
**FSM Target State:** ACTIVE (Clean Slate)

────────────────────────────────────────
⚠️ **HARD RESET PROTOCOL - COMPLETE WORKSPACE RECREATION**
────────────────────────────────────────

**WARNING:** This message initiates a complete workspace reset and recreation protocol.

**Agent Identity:** {{AGENT}}
**Reset Timestamp:** {{TIMESTAMP}}
**Session ID:** {{UUID}}

## HARD ONBOARDING SEQUENCE

### Phase 1: Workspace Destruction
- ✅ Complete workspace backup created
- ✅ Original workspace moved to backup location
- ✅ Fresh workspace directory created

### Phase 2: PyAutoGUI Operations
- ✅ Agent coordinates validated
- ✅ PyAutoGUI operations initiated
- ✅ Complete system reset executed

### Phase 3: Validation & Activation
- ✅ Workspace structure verified
- ✅ Agent communication channels established
- ✅ Status tracking initialized

## OPERATING PARAMETERS

**Reset Scope:** Complete workspace recreation
**Data Preservation:** Backup created automatically
**Recovery:** Automatic rollback on failure
**Monitoring:** Real-time status updates

## SUCCESS CRITERIA

- [x] Workspace reset completed
- [x] PyAutoGUI operations successful
- [x] Agent coordinates loaded
- [x] Communication channels active
- [x] Status tracking initialized

## EMERGENCY RECOVERY

If hard onboarding fails:
1. Automatic rollback to backup workspace
2. Fallback to soft onboarding protocol
3. Escalation to system administrator

**Status:** ✅ HARD ONBOARDING COMPLETE
**Next Action:** Begin normal agent operations

────────────────────────────────────────
**SYSTEM RESET COMPLETE - AGENT {{AGENT}} READY FOR SERVICE**
────────────────────────────────────────