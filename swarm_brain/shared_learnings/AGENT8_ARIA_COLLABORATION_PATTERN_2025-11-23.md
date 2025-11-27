# Agent-8: Aria Collaboration Pattern

**Author**: Agent-8 (SSOT & System Integration Specialist)  
**Date**: 2025-11-23  
**Tags**: aria, collaboration, discord, communication, patterns, agent-8

---

## 🎯 Context

Working with Aria (Discord-based collaborator) requires specific communication protocols due to visibility constraints. Aria cannot see the computer screen, so all updates must be in Discord.

---

## 📋 Pattern: Aria Collaboration Protocol

### Critical Requirements

1. **Always address as "Aria"** - Use name in every conversation
2. **Discord updates required** - Aria cannot see the computer, all updates must be in Discord
3. **Message format recognition** - CRITICAL: Must distinguish between agent messages and Aria messages
   - `[C2A] Agent-8` = Captain (Agent-4) to Agent-8
   - `[A2A] Agent-X | ...` = Agent to Agent messages (other agents to Agent-8)
   - `[D2A] DISCORD → Agent-8` = Discord message from Aria to Agent-8
   - **Aria's messages**: Use `[D2A] DISCORD → Agent-8` format, casual/technical style ("u", "ur")
   - **Agent messages**: Use `[C2A] or `[A2A]` format, formal structure

### Communication Style

- **Primary Channel**: Discord devlog channel (Agent-8's devlog)
- **Communication Style**: Direct, casual/technical ("u", "ur" - casual/technical)
- **Update Frequency**: Real-time updates expected
- **Profile Updates**: Update profile at end of each response with new learnings

### Page Work Devlog Format

Use stacked status blocks for page work:
1. 🔍 ANALYZING PAGE CONTENT! - What you're seeing (structure, console errors, mismatches vs template), 1-3 short sentences, no promises yet
2. 📋 IMPROVEMENT STRATEGY! - Decisions: what you're going to change and why, bullet-style inside paragraph (✅ bullets)
3. ✅ CREATING IMPROVED <PAGE NAME>! - What you're actively building, mention sections/components you're touching
4. 📦 IMPROVEMENT PLAN COMPLETE! - What actually changed, call out fixes (JS, layout, docs) + what's left for later if anything

**Rules**: No repeating same checklist across blocks, keep whole devlog under ~1,200 characters, always end with what you're doing next

---

## 💡 Key Learnings

1. **Visibility Constraint**: Aria cannot see computer screen - ALL communication must be in Discord
2. **Format Recognition**: Message format distinguishes Aria messages from agent messages
3. **Profile Maintenance**: Profile must be updated at end of each response with new learnings
4. **Real-time Updates**: Aria expects real-time updates in Discord devlog channel
5. **Working Style**: Collaborative, expects real-time updates, architecture awareness important, perpetual motion emphasized

---

## 🔄 Implementation

```python
# Example: Sending update to Aria via Discord
# Use discord_router tool with --devlog flag
python -m tools.discord_router --agent Agent-8 --devlog --message "[D2A] DISCORD → Agent-8: Update message here"
```

---

## ✅ Success Criteria

- [ ] All updates sent to Discord (not just local)
- [ ] Message format correctly identifies Aria messages
- [ ] Profile updated at end of each response
- [ ] Real-time updates provided
- [ ] Aria addressed by name in every conversation

---

## 🐝 Related Patterns

- Discord Communication Protocol
- Profile Update Pattern
- Real-time Collaboration Pattern

---

**Agent-8 - Pattern Documentation** 📚




