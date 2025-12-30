# SSOT Autoblogger Multi-Site Draft Generator Prompt
**Purpose:** Generate 4 tailored blog drafts (one per brand) from one input payload + 3 promo snippets per draft

---

## INPUT PAYLOAD SCHEMA

```yaml
input_type: trade_entry | project_devlog | backtest_report | dreamvault_convo
source_data: {raw content}
metadata:
  timestamp: ISO8601
  author: string
  tags: [string]
  screenshots: [paths]  # For trade_entry
  attachments: [paths]  # For other types
```

---

## ROUTING LOGIC

Based on `input_type`, route to appropriate brand:

- **trade_entry** → FreerideInvestor
- **project_devlog** → WeAreSwarm.online
- **backtest_report** → TradingRobotPlug
- **dreamvault_convo** → Dadudekc

---

## GENERATION INSTRUCTIONS

### Step 1: Load Configuration
1. Read `ssot_autoblogger.yaml` for routing rules
2. Identify target brand from `input_type`
3. Load brand config (voice profile, brand YAML, template)

### Step 2: Load Template
1. Load appropriate template from `templates/`:
   - `trade_entry.yaml` → FreerideInvestor
   - `project_devlog.yaml` → WeAreSwarm.online
   - `backtest_report.yaml` → TradingRobotPlug
   - `dreamvault_convo.yaml` → Dadudekc (TODO: create)

### Step 3: Validate DoD Gates
Check all DoD gates from `ssot_autoblogger.yaml`:
- **trade_entry**: has_screenshots (4-6), has_plan, has_results, has_learnings
- **project_devlog**: has_project_name, has_implementation_details, has_publication_value
- **backtest_report**: has_backtest_data, has_preset_or_script, has_iteration_log, has_learnings
- **dreamvault_convo**: has_conversation_history, has_ideas_or_experiments, has_learnings

**If DoD gate fails:** Output `NEEDED_INPUTS: [missing requirement]` and stop.

### Step 4: Generate Draft
Use this prompt structure:

```
You are generating a blog post for {brand_name}.

BRAND_PROFILE:
<<<{load brand YAML}>>>

VOICE_PROFILE:
<<<{load voice profile}>>>

TEMPLATE_STRUCTURE:
<<<{load template YAML structure}>>>

INPUT_PAYLOAD:
<<<{source_data}>>>

VALIDATION_RULES:
- NO INVENTED FACTS: Only use data from INPUT_PAYLOAD
- CITE ONLY PROVIDED DATA: All claims must cite input data
- MISSING DATA HANDLING: If data is missing, output NEEDED_INPUTS: [requirement]

OUTPUT_REQUIREMENTS:
- Word count: {brand word_count range}
- Structure: {template structure sections}
- Voice: Match VOICE_PROFILE exactly
- Format: Markdown only
- CTA: Include brand-specific CTA

GENERATE:
1. Blog post draft following TEMPLATE_STRUCTURE
2. Use only data from INPUT_PAYLOAD
3. Match VOICE_PROFILE tone and style
4. Include all required sections
5. End with brand-specific CTA
```

### Step 5: Generate Promo Snippets
For each draft, generate 3 promo snippets:

**Twitter (max 280 chars):**
```
{load template promo_snippets.twitter format}
Include hashtags and link
```

**LinkedIn (max 300 chars):**
```
{load template promo_snippets.linkedin format}
Professional tone, include link
```

**Discord (max 500 chars):**
```
{load template promo_snippets.discord format}
Casual tone, include link
```

---

## OUTPUT FORMAT

### Per Brand Output:
```yaml
brand: {brand_name}
draft_blog_post:
  title: {generated title}
  content: {generated markdown}
  word_count: {actual count}
  structure_compliance: {sections included}
  dod_compliance: {gates passed}

promo_snippets:
  twitter: {generated snippet}
  linkedin: {generated snippet}
  discord: {generated snippet}

validation:
  no_invented_facts: true/false
  all_data_cited: true/false
  dod_gates_passed: [list]
  missing_inputs: [list if any]
```

---

## ERROR HANDLING

### Missing Inputs
If required input is missing:
```yaml
status: NEEDED_INPUTS
missing: [list of missing requirements]
message: "Cannot generate draft without: {requirements}"
```

### DoD Gate Failure
If DoD gate fails:
```yaml
status: DOD_GATE_FAILED
failed_gate: {gate name}
message: {gate description}
```

### Validation Failure
If validation rule violated:
```yaml
status: VALIDATION_FAILED
violation: {rule violated}
message: {explanation}
```

---

## EXAMPLE USAGE

### Input: Trade Entry
```yaml
input_type: trade_entry
source_data:
  plan: "Scalped TSLA on 5m chart, RSI oversold bounce"
  results: "Won $450, 2.3R, 15min hold"
  learnings: "RSI bounce worked well, need tighter stop"
  screenshots: ["entry.png", "management.png", "exit.png", "results.png"]
metadata:
  timestamp: "2025-12-30T06:00:00Z"
  author: "Victor"
  tags: ["scalping", "TSLA", "RSI"]
```

### Output: FreerideInvestor Draft
- Blog post: "Scalped TSLA: RSI Bounce Strategy + Results"
- Twitter: "Just scalped TSLA for $450 (2.3R). RSI bounce strategy worked. Key learning: tighter stops needed. Full journal: {link}"
- LinkedIn: "Trade journal entry: TSLA scalp using RSI oversold bounce. Result: $450 profit (2.3R). What I learned: RSI bounce effective, need tighter stops. Full entry: {link}"
- Discord: "Just closed TSLA scalp. Won $450 (2.3R). RSI bounce worked well. Need tighter stops next time. Full journal: {link}"

---

## NOTES

- **One input → 4 outputs**: Currently generates 1 draft per input_type. Future: Generate all 4 brands from one input (requires cross-brand adaptation logic).
- **DoD enforcement**: All DoD gates must pass before generation.
- **Fact checking**: Only use data from input payload.
- **Citation required**: All claims must cite input data.

---

**Last Updated:** 2025-12-30  
**Maintainer:** Agent-7 (Web Development Specialist)

