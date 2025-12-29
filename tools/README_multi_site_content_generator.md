# Multi-Site Content Generator

Generate formatted content for multiple sites from a single source entry using SSOT routing.

## Sites Supported

1. **dadudekc.com** - Personal builder voice (short lines, direct)
2. **freerideinvestor.com** - Trading journal format (requires 4-6 screenshots)
3. **tradingrobotplug.com** - Iteration/backtest format
4. **weareswarm.online** - Docs + implementation + promo

## Usage

### Basic Usage

```bash
python tools/multi_site_content_generator.py \
  --source "path/to/source.txt" \
  --screenshots img1.png img2.png img3.png img4.png \
  --output generated_content.json
```

### Direct Text Input

```bash
python tools/multi_site_content_generator.py \
  --source "Built a new trading bot. Used RSI and MACD signals. Entry at $100, exit at $105. Profit: $500." \
  --screenshots screenshot1.png screenshot2.png screenshot3.png screenshot4.png
```

### Python API

```python
from tools.multi_site_content_generator import MultiSiteContentGenerator

source = """
# Trading Bot Update

Built a new automated trading system using RSI and MACD indicators.
Entry: $100
Exit: $105
Profit: $500

What worked: RSI signals were accurate
What didn't: MACD lagged on fast moves
"""

generator = MultiSiteContentGenerator(
    source_payload=source,
    attachments={"screenshots": ["img1.png", "img2.png", "img3.png", "img4.png"]}
)

output = generator.generate_all()
print(output)
```

## Output Format

The generator produces JSON with content for each site:

```json
{
  "dadudekc": {
    "title": "...",
    "hook": "...",
    "bullets": {
      "idea": "...",
      "what_i_built": "...",
      "what_i_learned": "...",
      "proof": "...",
      "automation_offer": "..."
    },
    "resume_delta": {
      "skills_learned": [...],
      "artifact_shipped": "...",
      "links": [...]
    }
  },
  "freerideinvestor": {
    "title": "...",
    "setup": {
      "plan": "...",
      "signals_used": [...],
      "risk_rules": "..."
    },
    "execution": {
      "entry": "...",
      "management": "...",
      "exit": "..."
    },
    "results": {
      "p_l": "...",
      "what_worked": "...",
      "what_didnt": "..."
    },
    "learnings": "...",
    "cta": "signup / follow signals / tested system",
    "screenshots": [...]
  },
  "tradingrobotplug": {
    "title": "...",
    "thesis": "...",
    "backtest_or_test_summary": "...",
    "iteration_log": [
      {
        "change": "...",
        "reason": "...",
        "result": "...",
        "next_test": "..."
      }
    ],
    "cta": "scripts / presets / roadmap"
  },
  "weareswarm_online": {
    "title": "...",
    "what_we_built": "...",
    "how_it_works": "...",
    "repo_docs_structure": "...",
    "publish_promote_copy": "..."
  },
  "needed_inputs": [],
  "checklist": {
    "facts_traced_to_payload": true,
    "freerideinvestor_screenshots_4_6": true,
    "each_site_unique_angle_cta": true
  },
  "generated_at": "2025-12-29T..."
}
```

## Rules

### Dadudekc.com
- Short lines, direct, builder voice
- Must "sound just like me"
- No invented facts

### Freerideinvestor.com
- **Requires 4-6 screenshots** for 'done' status
- Trading journal format
- Must include entry, management, exit details

### TradingRobotPlug.com
- Always include iteration framing (what changed + result)
- Backtest/test summary required

### WeAreSwarm.online
- Turn work into docs + implementation notes + promo
- Include repo structure

## Validation

The generator validates inputs and outputs `needed_inputs` if information is missing:

```json
{
  "needed_inputs": [
    "freerideinvestor: Need 4-6 screenshots (currently 2)",
    "source_payload: Need substantial content (min 50 chars)"
  ]
}
```

## Extraction Logic

The generator uses pattern matching to extract information from source payload:

- **Titles**: First non-empty line or markdown headers
- **Ideas/Goals**: Patterns like "idea:", "goal:", "objective:"
- **What Built**: Patterns like "built", "created", "implemented"
- **Learnings**: Patterns like "learned", "discovered", "found"
- **Trading Data**: Entry, exit, P/L, signals, risk rules
- **Iterations**: Change, reason, result, next test
- **Links**: URLs extracted via regex

If information cannot be extracted, fields contain `"NEEDED_INPUT: [field] from source_payload"`.

## SSOT Routing

All content is generated from a single source entry (SSOT principle):
- One source payload → Multiple site formats
- No invented facts
- All facts traced to source_payload
- Missing information explicitly marked as NEEDED_INPUT

