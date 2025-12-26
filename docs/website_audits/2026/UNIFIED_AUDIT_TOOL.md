# Unified Website Audit Tool

**Created:** 2025-12-25  
**Author:** Agent-6 (Coordination & Communication Specialist)  
**Status:** ✅ Active - Replaces all previous audit tools

---

## Overview

The `unified_website_audit.py` tool consolidates all website audit functionality into a single, comprehensive tool that combines:

1. **Grade Card YAML-Based Scoring** (from `comprehensive_grade_card_audit.py`)
   - Reads and scores grade card YAML files
   - Category-by-category scoring with weighted points
   - P0/P1/P2 priority classification

2. **Real-Time Website Analysis** (from `enhanced_grade_card_audit.py`)
   - Live website scraping and analysis
   - Technical metrics validation
   - Automated checks for SEO, accessibility, conversion elements

3. **Technical Metrics** (Performance, SEO, Accessibility, Conversion, Mobile)
   - Performance: Load time, page size
   - SEO: Meta tags, Open Graph, Schema.org, H1 structure
   - Accessibility: Image alt text coverage
   - Conversion: Forms, chat widgets, GA4, Facebook Pixel
   - Mobile: Viewport meta tag validation

---

## Usage

```bash
# Audit all revenue engine websites (default)
python tools/unified_website_audit.py

# Audit specific websites
python tools/unified_website_audit.py --websites freerideinvestor.com dadudekc.com

# Custom websites directory
python tools/unified_website_audit.py --websites-dir /path/to/websites

# Custom output directory
python tools/unified_website_audit.py --output-dir /path/to/reports
```

---

## Output

The tool generates:
- **JSON Report**: `reports/unified_website_audit_YYYYMMDD_HHMMSS.json`
- **Console Summary**: Overall scores, letter grades, recommendation counts

### Report Structure

```json
{
  "timestamp": "2025-12-25T...",
  "audit_type": "unified_website_audit",
  "websites_audited": 4,
  "average_score": 46.75,
  "websites": {
    "freerideinvestor.com": {
      "website": "freerideinvestor.com",
      "url": "https://freerideinvestor.com",
      "audit_date": "...",
      "status": "complete",
      "real_time_analysis": { ... },
      "technical_metrics": {
        "performance": { "score": 100.0, ... },
        "seo": { "score": 33.33, ... },
        "accessibility": { "score": 0.0, ... },
        "conversion": { "score": 25.0, ... },
        "mobile": { "score": 100.0, ... }
      },
      "grade_card": { ... },  // If grade card YAML exists
      "overall_score": 51.67,
      "letter_grade": "D",
      "recommendations": [ ... ]
    }
  }
}
```

---

## Deprecated Tools

The following tools have been **merged and deleted**:

- ❌ `comprehensive_grade_card_audit.py` - Merged into unified tool
- ❌ `enhanced_grade_card_audit.py` - Merged into unified tool
- ❌ `improved_grade_card_audit.py` - Merged into unified tool

**All functionality is now in `unified_website_audit.py`**

---

## Features

### Grade Card Scoring
- Reads YAML grade card files
- Calculates weighted category scores
- Identifies P0/P1/P2 priority fixes
- Extracts gap analysis and fix recommendations

### Real-Time Analysis
- HTTP request to live website
- HTML parsing with BeautifulSoup
- Automated detection of:
  - Analytics tracking (GA4, GTM, Pixel)
  - Chat widgets (Intercom, Crisp, Tawk.to)
  - SEO elements (meta tags, schema, canonical)
  - Accessibility (alt text, semantic HTML)
  - Performance metrics (load time, page size)

### Combined Scoring
- Grade card score (if YAML exists)
- Technical metrics score (always calculated)
- Overall score: Average of all scores
- Letter grade: A (90+), B+ (80+), B (70+), C (60+), D (50+), F (<50)

### Recommendations
- Performance optimizations
- SEO improvements
- Accessibility fixes
- Conversion optimization
- Analytics setup
- Grade card-based fixes

---

## Example Output

```
📊 Unified Audit Complete!
   Websites: 4
   Average Score: 46.75/100
   Report: reports/unified_website_audit_20251225_185011.json

freerideinvestor.com:
  Overall Score: 51.67/100 (Grade D)
  Technical Score: 51.7/100
  Recommendations: 3

dadudekc.com:
  Overall Score: 45.0/100 (Grade F)
  Technical Score: 45.0/100
  Recommendations: 4

tradingrobotplug.com:
  Overall Score: 40.33/100 (Grade F)
  Technical Score: 40.3/100
  Recommendations: 5

crosbyultimateevents.com:
  Overall Score: 50.0/100 (Grade D)
  Technical Score: 50.0/100
  Recommendations: 4
```

---

## Technical Requirements

- Python 3.7+
- `requests` library (HTTP requests)
- `beautifulsoup4` library (HTML parsing)
- `pyyaml` library (YAML parsing)
- Internet connection (for real-time analysis)

Install dependencies:
```bash
pip install requests beautifulsoup4 pyyaml
```

---

## Migration Guide

### Old Tool → New Tool

**Before:**
```bash
python tools/comprehensive_grade_card_audit.py --websites-dir /path/to/websites
python tools/enhanced_grade_card_audit.py
python tools/improved_grade_card_audit.py --site freerideinvestor.com --url https://freerideinvestor.com
```

**After:**
```bash
python tools/unified_website_audit.py --websites-dir /path/to/websites
python tools/unified_website_audit.py
python tools/unified_website_audit.py --websites freerideinvestor.com:https://freerideinvestor.com
```

---

*Created by Agent-6 | Unified Audit Tool | 2025-12-25*

