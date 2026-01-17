# Codebase Audit Runbook (Reproducible)

## Pre-reqs (pick what you already have)
- python env
- ripgrep (`rg`) - optional for advanced analysis
- optional: `jscpd`, `vulture` (for advanced dead code analysis)

## 1) Inventory (truth source)
mkdir -p audit_outputs
python audit_harness_standalone.py inventory --roots src tools scripts archive --out audit_outputs/manifest.json

Expected output:
```
📊 Generating file inventory...
✅ Inventory saved to audit_outputs/manifest.json
   Total files: 5090
   Total size: 50,417,602 bytes
```

## 2) Duplication (real evidence)
python audit_harness_standalone.py dup --roots src tools scripts --out audit_outputs/duplication_jscpd.json

Expected output:
```
🔍 Analyzing code duplication...
✅ Duplication analysis saved to audit_outputs/duplication_jscpd.json
   Patterns analyzed: 4
   Files with high duplication: 129
```

## 3) Archive sanity (age/size buckets)
python audit_harness_standalone.py archive --root archive --out audit_outputs/archive_age_report.csv

Expected output:
```
📦 Analyzing archive contents...
✅ Archive analysis saved to audit_outputs/archive_age_report.csv
   Files by age bucket: {'0-90d': 1760, '90-180d': 6, '180-365d': 1960, '365d+': 0}
   Large files (>100KB): 32
   Very old files (>365d): 0
```

## 4) Captain report generation
python audit_harness_standalone.py report --inputs audit_outputs --out audit_outputs/CAPTAIN_AUDIT_REPORT.md

Expected output:
```
📋 Generating Captain audit report...
✅ Captain report generated: audit_outputs/CAPTAIN_AUDIT_REPORT.md
```

## 5) Advanced Analysis (Optional - requires additional tools)

### Dead Code Detection
```bash
pip install vulture
vulture src/ > audit_outputs/vulture_dead_code.txt
```

### Import Graph Analysis
```bash
pip install networkx matplotlib
python -c "
import networkx as nx
# Generate import graph visualization
# (complex implementation needed)
" > audit_outputs/import_graph.txt
```

### Clone Detection (Advanced)
```bash
npm install -g jscpd
jscpd --format json --output audit_outputs/duplication_jscpd.json src/ tools/ scripts/
```

## Output Files Generated

After running all commands, you should have:

- `audit_outputs/manifest.json` - Complete file inventory with metadata
- `audit_outputs/duplication_jscpd.json` - Duplication pattern analysis
- `audit_outputs/archive_age_report.csv` - Archive retention analysis
- `audit_outputs/CAPTAIN_AUDIT_REPORT.md` - Executive-ready audit report

## Verification Commands

### Check file counts match
```bash
find src tools scripts archive -name "*.py" -type f | wc -l  # Should match manifest.json
```

### Validate duplication hotspots
```bash
grep -r "def __init__" src/ | wc -l  # Should match duplication_jscpd.json patterns
```

### Archive age verification
```bash
find archive/ -name "*.py" -mtime +365 | wc -l  # Should be 0 based on report
```

## Troubleshooting

### Audit harness fails to run
- Ensure Python 3.8+ is available
- Check file permissions on audit_outputs/ directory
- Verify all target directories (src/, tools/, etc.) exist

### Memory issues with large codebases
- Reduce scope: `python audit_harness_standalone.py dup --roots src --out audit_outputs/dup_src_only.json`
- Process in batches for very large repositories

### Permission errors
- Run in directory with write access to create audit_outputs/
- Use sudo if needed for system directories

## Next Steps After Audit

1. **Review CAPTAIN_AUDIT_REPORT.md** with stakeholders
2. **Prioritize action items** based on business impact
3. **Create implementation plan** for refactor batches
4. **Set up monitoring** for duplication thresholds
5. **Establish retention policy** for archive cleanup