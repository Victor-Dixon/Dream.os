# Reusable Prompt Template for Consolidation Tasks

**Copy and paste this prompt when you need to execute consolidation merges:**

---

## PROMPT:

```
I need to execute GitHub repository consolidation merges. Here's the situation:

**Context:**
- We have pending consolidation tasks that were blocked by GitHub API rate limits
- We've discovered that using pure git operations (clone, merge, push) bypasses ALL API rate limits
- These are my own repositories, so git operations have unlimited capacity

**Current Status:**
- Phase 0 merges: 2 successful (focusforge, tbowtactics), 2 blocked (repo access issues)
- Group 7: gpt_automation → selfevolving_ai (blocked - repo not found)
- GPT patterns from Auto_Blogger: ✅ Already extracted

**Available Tools:**
- `tools/repo_safe_merge.py` - Now uses git operations as PRIMARY method (no rate limits)
- `tools/git_based_merge_primary.py` - Standalone git-based merge tool
- `tools/unified_github_pr_creator.py` - Unified PR creation with auto-fallback

**What I Need:**
1. Execute remaining consolidation merges using git-based method (NO API RATE LIMITS)
2. For any successful merges, generate PR URLs for manual creation
3. Document blockers clearly (repository access issues vs method issues)
4. Update consolidation tracking

**My Approach:**
- Action first, execution only
- Think what I would do if this project were mine
- Execute immediately without asking for permission
- Use git operations to bypass rate limits completely

**Pending Tasks to Execute:**
- [LIST SPECIFIC MERGES HERE]
- Example: "gpt_automation → selfevolving_ai", "trade-analyzer → trading-leads-bot", etc.

Execute all pending merges using the git-based method. Report results immediately.
```

---

## EXAMPLE USAGE:

```
I need to execute GitHub repository consolidation merges. Here's the situation:

**Context:**
- We have pending consolidation tasks that were blocked by GitHub API rate limits
- We've discovered that using pure git operations (clone, merge, push) bypasses ALL API rate limits
- These are my own repositories, so git operations have unlimited capacity

**Current Status:**
- Phase 0 merges: 2 successful (focusforge, tbowtactics), 2 blocked (repo access issues)
- Group 7: gpt_automation → selfevolving_ai (blocked - repo not found)
- GPT patterns from Auto_Blogger: ✅ Already extracted

**Available Tools:**
- `tools/repo_safe_merge.py` - Now uses git operations as PRIMARY method (no rate limits)
- `tools/git_based_merge_primary.py` - Standalone git-based merge tool
- `tools/unified_github_pr_creator.py` - Unified PR creation with auto-fallback

**What I Need:**
1. Execute remaining consolidation merges using git-based method (NO API RATE LIMITS)
2. For any successful merges, generate PR URLs for manual creation
3. Document blockers clearly (repository access issues vs method issues)
4. Update consolidation tracking

**My Approach:**
- Action first, execution only
- Think what I would do if this project were mine
- Execute immediately without asking for permission
- Use git operations to bypass rate limits completely

**Pending Tasks to Execute:**
- trade-analyzer → trading-leads-bot
- UltimateOptionsTradingRobot → trading-leads-bot
- TheTradingRobotPlug → trading-leads-bot
- content → Auto_Blogger
- FreeWork → Auto_Blogger

Execute all pending merges using the git-based method. Report results immediately.
```

---

## QUICK VERSION (Minimal Context):

```
Execute GitHub consolidation merges using git-based method (NO API RATE LIMITS):

Pending merges:
- [source_repo] → [target_repo]
- [source_repo] → [target_repo]

Use tools/repo_safe_merge.py with --execute flag. Action first, execution only.
Report PR URLs for successful merges.
```

---

## FOR SPECIFIC AGENT ASSIGNMENTS:

```
As Agent-7 (Web Development Specialist), execute my consolidation assignment:

**Assignment:**
- Phase 0: [list repos]
- Group 7: [list repos]

**Method:** Git-based operations (NO API RATE LIMITS)
**Tool:** tools/repo_safe_merge.py --execute
**Approach:** Action first, execution only

Execute all merges immediately. Update consolidation_progress.json with results.
```

---

**Note:** Customize the "Pending Tasks to Execute" section with your specific merges before using.

