# A++ Closure Standard Documentation & Enforcement

## Problem

The A++ closure standard exists but is not discoverable by other agents or future agents. Agents need:

- Clear documentation of the standard
- Validation to ensure compliance
- Templates to follow
- Integration into existing systems

## Solution

Create a multi-layered system: workspace rules (discoverable), updated canonical prompt (enforced), validation tool (automated), and template files (easy to use).

## Implementation

### 1. Workspace Rules Documentation

**File:** `.cursor/rules/session-closure.mdc`Create new rule file that:

- Documents A++ closure format with examples
- Lists violations (no "next steps", no narration, etc.)
- Shows correct vs incorrect examples
- References canonical prompt location
- Auto-applies to all agents via workspace rules system

**Key sections:**

- Required fields (Task, Actions, Artifacts, Verification, Public Build Signal, Status)
- Forbidden elements (next steps, speculation, narration)
- Verification requirements
- Public build signal format (single line, human-readable)

### 2. Update Canonical Closure Prompt

**File:** `src/services/onboarding/soft/canonical_closure_prompt.py`Update `CANONICAL_CLOSURE_PROMPT` to:

- Match A++ format exactly (no "next steps" section)
- Include explicit verification block requirements
- Require single-line public build signal
- Remove any "next steps" language
- Add examples of correct format

**Changes:**

- Remove "Next priorities" from passdown.json section
- Add explicit "Verification" block with proof requirements
- Add "Public Build Signal" as mandatory single line
- Remove any future work references

### 3. Create Validation Tool

**File:** `tools/validate_closure_format.py`Create tool that:

- Reads closure document (markdown or text)
- Validates required fields exist
- Checks for forbidden elements ("next steps", speculation words)
- Validates public build signal is single line
- Returns pass/fail with specific violations
- Can be run pre-commit or in CI

**Validation checks:**

- Required fields: Task, Actions, Artifacts, Verification, Public Build Signal, Status
- Forbidden: "next steps", "TODO", "future", speculation words
- Format: Public build signal is single line
- Verification: Contains proof/evidence

### 4. Create Template File

**File:** `templates/session-closure-template.md`Create template that agents can copy:

- Pre-filled with required sections
- Comments explaining each section
- Examples of correct content
- Placeholder text to replace
- Links to full documentation

**Template structure:**

```markdown
# A++ Session Closure

- **Task:** [Brief task description]
- **Project:** [Project/repo name]

- **Actions Taken:**
    - [Bullet 1]
    - [Bullet 2]

- **Artifacts Created / Updated:**
    - [Exact file paths]

- **Verification:**
    - [Proof/evidence bullets]

- **Public Build Signal:**
  [Single line, human-readable description]

- **Status:**
  ✅ Ready
```



### 5. Update Onboarding References

**Files to update:**

- `src/services/onboarding/soft/steps.py` - Reference closure standard
- `docs/onboarding/` - Add closure section
- `.cursor/rules/README.md` - Document new rule file

Add references to:

- Where to find closure standard
- How to use template
- How to validate before submitting

### 6. Swarm Brain Entry (Optional)

**Action:** Create Swarm Brain entry documenting:

- A++ closure standard
- Why it exists (build-in-public, state preservation)
- How to use it
- Examples of correct closures

## Files Created/Modified

**New Files:**

- `.cursor/rules/session-closure.mdc` - Workspace rule
- `tools/validate_closure_format.py` - Validation tool
- `templates/session-closure-template.md` - Template file

**Modified Files:**

- `src/services/onboarding/soft/canonical_closure_prompt.py` - Update to A++ format
- `src/services/onboarding/soft/steps.py` - Add closure reference
- `.cursor/rules/README.md` - Document new rule

## Verification

After implementation:

- ✅ New agents can discover standard via `.cursor/rules/`
- ✅ Validation tool catches violations
- ✅ Template makes it easy to follow
- ✅ Canonical prompt enforces format
- ✅ Onboarding references standard

## Success Criteria

- Any agent can find A++ closure standard in workspace rules
- Validation tool catches format violations
- Template reduces errors