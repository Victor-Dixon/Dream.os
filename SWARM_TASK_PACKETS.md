# 🤖 SWARM TASK PACKETS

**Purpose:** Ready-to-execute directives for Swarm agents. No ambiguity.

**Format:** Each packet is self-contained and executable.

**Last Updated:** 2025-12-16

---

## 📋 PACKET STRUCTURE

Each packet contains:
- **Objective:** What to achieve
- **Scope:** What's included/excluded
- **Output:** Deliverable format
- **Constraints:** Boundaries and rules
- **Context:** Why this matters

---

## PACKET 1: SITE AUDIT & PURPOSE MAP

**Priority:** HIGH  
**Owner:** Swarm Agent (Site Auditor)  
**Timeline:** 2-3 days  
**Status:** 🔴 READY TO EXECUTE

### Objective
Audit all 11 websites and create a comprehensive purpose map documenting:
- What each site is for
- Current funnel stage
- Primary conversion goal
- Content status
- Technical status

### Scope
**Include:**
- All sites in repository/domain list
- Current content audit
- Funnel structure analysis
- CTA identification
- Analytics setup status

**Exclude:**
- Redesigns or major changes
- New feature development
- Marketing campaigns

### Output
Create `docs/sites/SITE_AUDIT_2025-12-16.md` with:

```markdown
# Site Audit Report

## Site Inventory
| Site | Purpose | Funnel Stage | CTA | Status | Notes |
|------|---------|--------------|-----|--------|-------|
| freerideinvestor.com | Trading education | Interest | Email signup | Active | Blog live |
| ... | ... | ... | ... | ... | ... |

## Findings
- X sites have complete funnels
- Y sites need CTA definition
- Z sites are in maintenance mode

## Recommendations
- Prioritize sites A, B, C for active funnel
- Sites D, E can enter maintenance mode
```

### Constraints
- **No changes to sites** - audit only
- **Document current state** - not future plans
- **Use existing Swarm knowledge** - don't research from scratch
- **One file output** - consolidated report

### Context
Victor needs clarity on all 11 sites to:
1. Decide which funnel is "active"
2. Assign maintenance vs active status
3. Update Swarm brain with accurate site purposes

### Execution Directive
```
Agent: Site Auditor
Task: Audit all websites in repository
Output: Single markdown file with site inventory table
Time: 2-3 days
No code changes, documentation only
```

---

## PACKET 2: FUNNEL TEMPLATE STANDARDIZATION

**Priority:** MEDIUM  
**Owner:** Swarm Agent (Funnel Architect)  
**Timeline:** 3-5 days  
**Status:** 🔴 READY TO EXECUTE

### Objective
Create a standardized funnel structure template that can be applied across all sites, ensuring:
- Consistent CTA placement
- Standard follow-up mechanisms
- Unified analytics tracking
- Reusable components

### Scope
**Include:**
- Template structure (HTML/CSS/JS if needed)
- CTA framework documentation
- Follow-up flow documentation
- Analytics integration guide

**Exclude:**
- Site-specific customizations
- Content creation
- Marketing campaigns

### Output
Create `docs/funnels/FUNNEL_TEMPLATE_STANDARD.md` with:
- Template structure
- CTA placement rules
- Follow-up sequence template
- Analytics setup guide
- Implementation checklist

### Constraints
- **Template only** - not implementation
- **Reusable** - works across different site types
- **Documentation first** - code second
- **No breaking changes** - existing sites unaffected

### Context
Victor needs consistent funnel structure across all sites to:
1. Reduce decision fatigue
2. Enable Swarm to clone patterns
3. Standardize conversion tracking
4. Speed up new site setup

### Execution Directive
```
Agent: Funnel Architect
Task: Create standardized funnel template documentation
Output: Template guide + implementation checklist
Time: 3-5 days
Focus on structure, not content
```

---

## PACKET 3: BLOG → SOCIAL CONTENT REPURPOSING

**Priority:** MEDIUM  
**Owner:** Swarm Agent (Content Repurposer)  
**Timeline:** Ongoing  
**Status:** 🔴 READY TO EXECUTE

### Objective
Automatically repurpose blog posts into social media content:
- Extract key points
- Create social post variations
- Format for Instagram/Facebook
- Maintain consistent messaging

### Scope
**Include:**
- Existing blog posts (FreeRideInvestor, etc.)
- Social post generation
- Formatting for platforms
- Scheduling suggestions

**Exclude:**
- New blog content creation
- Social media posting (manual for now)
- Engagement management

### Output
For each blog post, create:
- `content/social/YYYY-MM-DD-instagram.md`
- `content/social/YYYY-MM-DD-facebook.md`
- `content/social/YYYY-MM-DD-twitter.md`

Each file contains:
- Post text (formatted)
- Suggested image/visual
- Hashtags
- CTA

### Constraints
- **Repurpose only** - don't create new content
- **Maintain voice** - match blog tone
- **One post per platform** - not multiple variations
- **Manual posting** - Swarm doesn't post, just creates

### Context
Victor's marketing approach is "build in public + explain clearly". Blog posts are the source, social is distribution.

### Execution Directive
```
Agent: Content Repurposer
Task: Repurpose existing blog posts into social content
Output: Platform-specific post files
Time: Ongoing (process each new blog post)
No posting, just content creation
```

---

## PACKET 4: FREE RIDE INVESTOR FUNNEL OPTIMIZATION

**Priority:** HIGH (if chosen as active funnel)  
**Owner:** Swarm Agent (Funnel Optimizer)  
**Timeline:** 7-14 days  
**Status:** ⏸️ PENDING VICTOR DECISION

### Objective
Optimize FreeRideInvestor.com funnel for conversion:
- Review current CTA clarity
- Improve follow-up sequence
- Add lead magnet
- Set up email sequence
- Track drop-off points

### Scope
**Include:**
- CTA optimization
- Email sequence setup
- Lead magnet creation
- Analytics implementation
- A/B testing setup

**Exclude:**
- Complete redesign
- New content creation (repurpose existing)
- Marketing campaigns

### Output
- Updated funnel pages
- Email sequence templates
- Lead magnet document
- Analytics dashboard
- Conversion report

### Constraints
- **Work within existing design** - no major redesigns
- **Repurpose existing content** - don't create new
- **Test before deploy** - staging first
- **Document changes** - changelog required

### Context
FreeRideInvestor is a candidate for "active funnel" status. If chosen, this packet executes.

### Execution Directive
```
Agent: Funnel Optimizer
Task: Optimize FreeRideInvestor funnel (pending approval)
Output: Optimized pages + email sequence + analytics
Time: 7-14 days
Wait for Victor's "active funnel" decision
```

---

## PACKET 5: KIKI SITE PROTOTYPE SUPPORT

**Priority:** HIGH  
**Owner:** Swarm Agent (Site Builder)  
**Timeline:** 3-5 days (after Victor chooses theme)  
**Status:** ⏸️ PENDING VICTOR THEME SELECTION

### Objective
Build Kiki's mobile bartending website prototype:
- Implement chosen theme
- Upload existing photos
- Create booking/contact flow
- Write initial copy (from outline)
- Position as incubator case study

### Scope
**Include:**
- Theme implementation
- Photo uploads
- Booking form
- Contact flow
- Basic copy (from Victor's outline)

**Exclude:**
- Logo design (already done)
- Photo editing (use as-is)
- Content strategy (Victor provides)

### Output
- Live prototype site
- Booking form functional
- Contact flow working
- Case study page ready

### Constraints
- **Match logo** - theme must align
- **Use existing photos** - no new photography
- **Follow funnel template** - use Packet 2 template
- **Quick prototype** - not final polish

### Context
This is proof of concept for incubator service. High priority for Victor.

### Execution Directive
```
Agent: Site Builder
Task: Build Kiki site prototype (after theme selection)
Output: Functional prototype site
Time: 3-5 days
Wait for Victor to select theme/template
```

---

## PACKET 6: SWARM CONTEXT UPDATE

**Priority:** HIGH  
**Owner:** Swarm Agent (System Maintainer)  
**Timeline:** 1 day  
**Status:** 🔴 READY TO EXECUTE

### Objective
Update Swarm brain/context with:
- Current site purposes (from Packet 1)
- Active priorities
- Family team structure
- Collaboration boundaries
- Swarm scope limits

### Scope
**Include:**
- Site purpose updates
- Priority list
- Team structure
- Boundaries and rules

**Exclude:**
- Code changes
- New features
- External integrations

### Output
Updated Swarm context files:
- `swarm/context/sites.md`
- `swarm/context/priorities.md`
- `swarm/context/boundaries.md`

### Constraints
- **Update only** - don't restructure
- **Use Packet 1 results** - wait for site audit
- **Clear boundaries** - no ambiguity
- **One-time update** - not ongoing

### Context
Swarm needs current context to execute other packets correctly.

### Execution Directive
```
Agent: System Maintainer
Task: Update Swarm context with current state
Output: Updated context files
Time: 1 day
Wait for Packet 1 (site audit) to complete first
```

---

## PACKET 7: GITHUB MIGRATION SUPPORT

**Priority:** MEDIUM  
**Owner:** Swarm Agent (DevOps)  
**Timeline:** 2-3 days  
**Status:** ⏸️ PENDING VICTOR REPO LIST

### Objective
Migrate selected repositories to new GitHub account:
- Identify repos to migrate
- Update remote URLs
- Clean up old account references
- Verify all connections work

### Scope
**Include:**
- Repo migration
- Remote URL updates
- Reference cleanup
- Verification

**Exclude:**
- Code changes
- New repos
- External service updates

### Output
- Migrated repos
- Updated documentation
- Cleanup report

### Constraints
- **Only selected repos** - Victor decides which
- **No code changes** - migration only
- **Test everything** - verify after migration
- **Document changes** - update all references

### Context
Old GitHub account was flagged as spam. Need clean migration.

### Execution Directive
```
Agent: DevOps
Task: Migrate selected repos to new GitHub (pending list)
Output: Migrated repos + cleanup report
Time: 2-3 days
Wait for Victor to provide repo priority list
```

---

## 📊 PACKET EXECUTION ORDER

1. **Packet 6** (Swarm Context Update) - Foundation
2. **Packet 1** (Site Audit) - Information gathering
3. **Packet 2** (Funnel Template) - Standardization
4. **Packet 3** (Content Repurposing) - Ongoing
5. **Packet 4** (FreeRideInvestor) - If chosen as active
6. **Packet 5** (Kiki Site) - After theme selection
7. **Packet 7** (GitHub Migration) - When ready

---

## 🎯 HOW TO USE THESE PACKETS

1. **Review packets** - Understand what each does
2. **Prioritize** - Which packets execute first?
3. **Assign to Swarm** - Copy packet directive to Swarm
4. **Monitor progress** - Check outputs
5. **Iterate** - Create new packets as needed

---

## 📝 CREATING NEW PACKETS

When Victor identifies new Swarm tasks:

1. Use this packet structure
2. Define clear objective
3. Set boundaries (what's excluded)
4. Specify output format
5. Add execution directive

**Template:**
```markdown
## PACKET X: [TASK NAME]

**Priority:** [HIGH/MEDIUM/LOW]
**Owner:** Swarm Agent ([Role])
**Timeline:** [X days]
**Status:** [READY/PENDING]

### Objective
[What to achieve]

### Scope
**Include:** [What's in scope]
**Exclude:** [What's out of scope]

### Output
[Deliverable format]

### Constraints
[Boundaries and rules]

### Context
[Why this matters]

### Execution Directive
```
[Copy-paste ready directive for Swarm]
```
```

---

**Remember:** Packets are self-contained. Swarm can execute without asking questions if packet is complete.

