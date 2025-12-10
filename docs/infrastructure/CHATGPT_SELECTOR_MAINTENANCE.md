# ChatGPT Selector Maintenance Guide

**Author**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-12-10  
**Status**: Active Maintenance Documentation  
**Priority**: HIGH - Critical for Thea Automation Reliability

---

## 🎯 **Purpose**

ChatGPT frequently updates its UI, which can break automation selectors. This guide provides systematic procedures for maintaining and updating selectors to keep Thea automation functional.

---

## 🔍 **Quick Diagnosis**

### **Symptoms of Selector Failure**

- `_find_prompt_textarea()` returns `None`
- `_find_send_button()` returns `None`
- Automation fails with "Element not found" errors
- Debug logs show "All textarea discovery methods failed"

### **Immediate Actions**

1. **Run Debug Tool**: Use `tools/thea/debug_chatgpt_elements.py` to inspect current page structure
2. **Check Logs**: Review debug output from `TheaBrowserService` for selector attempts
3. **Verify Authentication**: Ensure authentication is working before debugging selectors

---

## 🛠️ **Step-by-Step Maintenance Procedure**

### **Step 1: Run Element Debug Tool**

```bash
python tools/thea/debug_chatgpt_elements.py
```

**What it does**:
- Opens ChatGPT page in visible browser
- Analyzes all textarea, contenteditable, and button elements
- Prints element attributes, locations, and visibility status
- Keeps browser open for manual inspection

**Output Analysis**:
- Look for elements with `location['y'] > 500` (near bottom of page)
- Identify elements with `visible: True` and `enabled: True`
- Note `data-testid`, `aria-label`, `id`, and `class` attributes

### **Step 2: Identify Correct Selectors**

**For Textarea/Input Elements**:
- Look for elements near bottom of page (Y position > 500)
- Check for `placeholder` containing "message", "ask", or "send"
- Verify `aria-label` attributes
- Note `data-testid` values if present

**For Send Button**:
- Look for button elements near the input area
- Check for `aria-label` containing "send" or "submit"
- Verify button is enabled and visible
- Note `data-testid` or `id` attributes

**Current Working Selectors** (as of 2025-12-10):
- **Input**: `div[contenteditable='true'][id='prompt-textarea']` (Primary)
- **Input**: `div[contenteditable='true'].ProseMirror` (Fallback)
- **Send Button**: `button[data-testid*='send-button']` (Primary)
- **Send Button**: `button[aria-label*='Send message']` (Fallback)

**Common Patterns**:
- `textarea[data-testid='prompt-textarea']`
- `div[contenteditable='true'][role='textbox']`
- `button[data-testid='send-button']`
- `button[aria-label*='Send']`
- `div.ProseMirror[contenteditable='true']` (Current ChatGPT)

### **Step 3: Update Selector Lists**

**File**: `src/infrastructure/browser/thea_browser_service.py`

**Location 1: Textarea Selectors** (Line ~295)
```python
def _get_prioritized_selectors(self) -> list[str]:
    """Get selectors prioritized by historical success rate."""
    base_selectors = [
        "textarea[data-testid='prompt-textarea']",  # Add new selector here
        # ... existing selectors ...
    ]
```

**Location 2: Send Button Selectors** (Line ~563)
```python
def _get_prioritized_send_selectors(self) -> list[str]:
    """Get send button selectors prioritized by historical success."""
    base_selectors = [
        "#composer-submit-button",  # Add new selector here
        # ... existing selectors ...
    ]
```

**Location 3: Fallback Selectors** (Line ~264)
```python
fallback_selectors = [
    "textarea",
    "div[contenteditable='true']",
    # Add new fallback patterns here
]
```

### **Step 4: Test Selector Updates**

**Test Procedure**:
1. Update selector lists with new selectors
2. Run `tools/thea/send_prompt_file.py` with a test prompt
3. Monitor debug logs for selector success
4. Verify prompt submission and response retrieval

**Validation**:
- ✅ Textarea found and ready
- ✅ Send button found and clickable
- ✅ Prompt submitted successfully
- ✅ Response retrieved correctly

### **Step 5: Clear Selector Cache (If Needed)**

**Cache Location**: `{cache_dir}/selector_success.json`

**When to Clear**:
- After major UI changes
- When selectors stop working despite updates
- When testing new selector priorities

**How to Clear**:
```bash
# Delete cache file
rm -f {cache_dir}/selector_success.json

# Or via Python
from pathlib import Path
cache_file = Path("{cache_dir}") / "selector_success.json"
if cache_file.exists():
    cache_file.unlink()
```

---

## 📋 **Maintenance Checklist**

### **When ChatGPT UI Changes**

- [ ] Run `debug_chatgpt_elements.py` to inspect new structure
- [ ] Identify new selectors for textarea and send button
- [ ] Update `_get_prioritized_selectors()` with new selectors
- [ ] Update `_get_prioritized_send_selectors()` with new send button selectors
- [ ] Add fallback patterns if needed
- [ ] Test automation with updated selectors
- [ ] Clear selector cache if necessary
- [ ] Update this documentation with new patterns
- [ ] Commit changes with descriptive message

### **Regular Maintenance**

- [ ] Review selector success rates monthly
- [ ] Check for deprecated selectors
- [ ] Test automation workflow quarterly
- [ ] Update documentation with new patterns
- [ ] Monitor debug logs for selector failures

---

## 🎯 **Best Practices**

### **Selector Priority**

1. **Specific Selectors First**: Use `data-testid`, `id`, or unique `aria-label` values
2. **Attribute Selectors**: Prefer `[data-testid='...']` over class selectors
3. **Fallback Patterns**: Keep broad patterns as last resort
4. **Success Caching**: Let auto-healing system learn successful selectors

### **Selector Format**

**Good Selectors**:
```python
"textarea[data-testid='prompt-textarea']"  # Specific and stable
"button[aria-label*='Send']"  # Flexible attribute matching
"div[contenteditable='true'][role='textbox']"  # Semantic role
```

**Avoid**:
```python
".some-class-name"  # Classes change frequently
"div:nth-child(5)"  # Position-based (fragile)
"button"  # Too generic (use as fallback only)
```

### **Testing Strategy**

1. **Test in Non-Headless Mode**: See what's happening visually
2. **Enable Debug Logging**: Monitor selector attempts
3. **Test Multiple Scenarios**: Different page states, loading times
4. **Verify Both Elements**: Textarea AND send button must work
5. **Test Full Workflow**: End-to-end automation test

---

## 🔧 **Debug Tools Reference**

### **debug_chatgpt_elements.py**

**Purpose**: Inspect current ChatGPT page structure

**Usage**:
```bash
python tools/thea/debug_chatgpt_elements.py
```

**Output**:
- Lists all textarea elements with attributes
- Lists all contenteditable divs
- Lists button elements (first 10)
- Lists role=button elements (first 10)
- Shows element locations and visibility

**Tips**:
- Look for elements near bottom of page (Y > 500)
- Check `visible: True` and `enabled: True`
- Note unique attributes (`data-testid`, `aria-label`, `id`)

### **analyze_chatgpt_selectors.py**

**Purpose**: Automated selector discovery and analysis

**Usage**:
```bash
python tools/thea/analyze_chatgpt_selectors.py
```

**Output**:
- Suggests potential selectors based on page analysis
- Scores selectors by relevance
- Identifies best candidates for automation

---

## 📊 **Auto-Healing System**

### **How It Works**

The auto-healing system uses a three-phase approach:

1. **Phase 1: Known Selectors** - Tries prioritized selectors from cache
2. **Phase 2: Dynamic Discovery** - Analyzes page for input-like elements
3. **Phase 3: Fallback Patterns** - Uses broad patterns as last resort

### **Success Rate Caching**

- Successful selectors are cached in `selector_success.json`
- Success rates tracked: `successes / attempts`
- Selectors prioritized by success rate
- Cache persists across sessions

### **When Auto-Healing Fails**

If all three phases fail:
1. Run `debug_chatgpt_elements.py` to inspect page
2. Identify new selectors manually
3. Update selector lists in code
4. Clear cache and test again

---

## 🚨 **Troubleshooting**

### **Problem: Selectors Not Working**

**Diagnosis**:
- Check if authentication is working
- Verify page has loaded completely
- Check debug logs for selector attempts
- Run debug tool to inspect current structure

**Solution**:
- Update selectors based on current UI
- Add new fallback patterns
- Clear selector cache
- Test with visible browser first

### **Problem: Selectors Work Intermittently**

**Diagnosis**:
- Check page loading timing
- Verify element visibility/readiness
- Review success rate cache

**Solution**:
- Increase wait times if needed
- Improve element readiness checks
- Update selector priorities based on success rates

### **Problem: Auto-Healing Not Learning**

**Diagnosis**:
- Check cache file permissions
- Verify cache directory exists
- Review cache file format

**Solution**:
- Ensure cache directory is writable
- Check cache file JSON format
- Clear and rebuild cache if corrupted

---

## 📝 **Documentation Updates**

When updating selectors, also update:

1. **This File**: Add new patterns to maintenance guide
2. **Code Comments**: Update docstrings with new selector patterns
3. **Debug Tools**: Enhance tools if new patterns discovered
4. **Test Cases**: Add tests for new selector patterns

---

## 🔗 **Related Files**

- `src/infrastructure/browser/thea_browser_service.py` - Main automation code
- `tools/thea/debug_chatgpt_elements.py` - Element inspection tool
- `tools/thea/analyze_chatgpt_selectors.py` - Selector analysis tool
- `tools/thea/send_prompt_file.py` - Automation test script
- `{cache_dir}/selector_success.json` - Selector success cache

---

## 🎯 **Quick Reference**

**Update Textarea Selectors**:
- File: `src/infrastructure/browser/thea_browser_service.py`
- Method: `_get_prioritized_selectors()` (line ~293)
- Add new selectors to `base_selectors` list

**Update Send Button Selectors**:
- File: `src/infrastructure/browser/thea_browser_service.py`
- Method: `_get_prioritized_send_selectors()` (line ~561)
- Add new selectors to `base_selectors` list

**Test Selectors**:
```bash
python tools/thea/debug_chatgpt_elements.py  # Inspect page
python tools/thea/send_prompt_file.py        # Test automation
```

**Clear Cache**:
```python
from pathlib import Path
cache_file = Path("{cache_dir}") / "selector_success.json"
cache_file.unlink() if cache_file.exists() else None
```

---

**Last Updated**: 2025-12-10
**Maintained By**: Agent-3 (Infrastructure & DevOps Specialist)
**Status**: Active - Recently tested and validated with current ChatGPT UI
**Current Selectors**: Working as of 2025-12-10 - div[contenteditable] + ProseMirror pattern

🐝 **WE. ARE. SWARM. ⚡🔥**

