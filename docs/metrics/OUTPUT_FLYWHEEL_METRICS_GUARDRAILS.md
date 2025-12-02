# Output Flywheel Metrics Guardrails

**Component**: Metrics Guardrail & Monitoring System  
**Author**: Agent-5 (Business Intelligence Specialist)  
**Status**: ✅ Complete  
**Date**: 2025-12-02  
**Priority**: HIGH

---

## 📊 Overview

The Metrics Guardrail system provides real-time monitoring and status indicators (RED/YELLOW/GREEN) for the Output Flywheel system. It ensures that artifacts are being created, documented, and published at expected rates.

---

## 🎯 Guardrail Metrics

### 1. Artifacts Per Week

**Description**: Total number of artifacts created per week

**Target**: 2+ artifacts per week (from shipping rhythm)

**Status Thresholds**:
- 🟢 **GREEN**: 2+ artifacts created
- 🟡 **YELLOW**: 1 artifact created (below target)
- 🔴 **RED**: 0 artifacts created (critical)

**Calculation**: Counts artifacts created in current week (Monday-Sunday)

**Action Required**:
- **YELLOW**: Review artifact creation pipeline
- **RED**: Immediate investigation - Output Flywheel may be stalled

---

### 2. Trading Days Documented

**Description**: Number of trading days with documented journal entries

**Target**: Document all trading days (80%+ of weekdays)

**Status Thresholds**:
- 🟢 **GREEN**: 80%+ of trading days documented
- 🟡 **YELLOW**: 50-79% of trading days documented
- 🔴 **RED**: <50% or zero trading days documented

**Calculation**: Counts trading sessions with journal entries vs. expected trading days in month

**Action Required**:
- **YELLOW**: Catch up on missing journal entries
- **RED**: Critical - trading documentation backlog

---

### 3. Publication Rate

**Description**: Percentage of artifacts successfully published to public platforms

**Target**: 90% publication rate

**Status Thresholds**:
- 🟢 **GREEN**: 90%+ publication rate
- 🟡 **YELLOW**: 75-89% publication rate
- 🔴 **RED**: <75% publication rate (critical: <50%)

**Calculation**: (Published artifacts / Total artifacts) × 100

**Action Required**:
- **YELLOW**: Investigate publication failures
- **RED**: Critical - publication pipeline issues

---

### 4. Missing Artifacts

**Description**: Work sessions with expected artifacts that are missing

**Target**: 0 missing artifacts

**Status Thresholds**:
- 🟢 **GREEN**: No missing artifacts
- 🟡 **YELLOW**: 1-3 sessions with missing artifacts
- 🔴 **RED**: 4+ sessions with missing artifacts

**Calculation**: Compares expected artifacts (from work_session.json) vs. actual files in outputs/artifacts/

**Action Required**:
- **YELLOW**: Review and regenerate missing artifacts
- **RED**: Critical - artifact generation pipeline failure

---

## 🚦 Status Definitions

### 🟢 GREEN Status

**Meaning**: System operating within target parameters

**Agent Response**:
- ✅ Continue normal operations
- ✅ Monitor trends
- ✅ Maintain current pace

### 🟡 YELLOW Status

**Meaning**: System below target but not critical

**Agent Response**:
- ⚠️ Review metrics and identify root cause
- ⚠️ Take corrective action within 24 hours
- ⚠️ Document findings
- ⚠️ Notify Captain if unable to resolve

### 🔴 RED Status

**Meaning**: Critical threshold breached - immediate action required

**Agent Response**:
- 🚨 **IMMEDIATE**: Stop other work and investigate
- 🚨 **IMMEDIATE**: Notify Captain via urgent message
- 🚨 **IMMEDIATE**: Document root cause and recovery plan
- 🚨 **IMMEDIATE**: Implement fix or workaround

---

## 🔧 Usage

### Check Guardrail Status

```bash
python systems/output_flywheel/metrics_monitor.py check
```

### Generate Report

```bash
python systems/output_flywheel/metrics_monitor.py report
```

Generates `guardrail_report.json` with full status details.

### Generate Alert Summary

```bash
python systems/output_flywheel/metrics_monitor.py alert
```

Generates formatted summary for devlog/Discord posting.

### JSON Output

```bash
python systems/output_flywheel/metrics_monitor.py json --output report.json
```

---

## 📋 Agent Response Protocol

### When Guardrail Shows YELLOW:

1. **Acknowledge**: Update status.json with guardrail status
2. **Investigate**: Review metrics and identify cause
3. **Plan**: Create recovery plan
4. **Act**: Implement fixes within 24 hours
5. **Report**: Update Captain with findings

### When Guardrail Shows RED:

1. **IMMEDIATE**: Stop other work
2. **IMMEDIATE**: Send urgent message to Captain
3. **IMMEDIATE**: Document root cause
4. **IMMEDIATE**: Implement emergency fix
5. **IMMEDIATE**: Provide status update every 2 hours until resolved

---

## 🔗 Integration Points

### Automated Monitoring

The guardrail system can be integrated with:
- **Cron jobs**: Daily/weekly status checks
- **CI/CD pipelines**: Pre-deployment validation
- **Discord bot**: Automatic status reporting
- **Devlog system**: Weekly status summaries

### Alert Hook

Use the alert summary in:
- Devlog posts
- Discord notifications
- Captain status reports
- Weekly reviews

---

## 📁 Configuration

Guardrail thresholds are configured in:
- `systems/output_flywheel/metrics_system.yaml` - Alert thresholds
- `systems/output_flywheel/metrics_monitor.py` - Status calculation logic

---

## 🔍 Monitoring Checklist

Daily:
- [ ] Check guardrail status
- [ ] Review any YELLOW/RED metrics
- [ ] Verify artifacts are being created

Weekly:
- [ ] Generate full guardrail report
- [ ] Post alert summary to devlog
- [ ] Review trends and adjust thresholds if needed

Monthly:
- [ ] Review threshold effectiveness
- [ ] Update targets based on performance
- [ ] Document lessons learned

---

## 🐛 Troubleshooting

### Missing Artifacts

**Symptom**: Guardrail shows missing artifacts

**Check**:
1. Verify work_session.json files exist
2. Check outputs/artifacts/ directory
3. Review artifact generation pipeline logs

**Fix**: Regenerate missing artifacts or update work_session.json

### Low Publication Rate

**Symptom**: Publication rate below threshold

**Check**:
1. Review publication queue status
2. Check for publication failures
3. Verify publication credentials/config

**Fix**: Resolve publication failures and retry

### Zero Artifacts

**Symptom**: No artifacts created this week

**Check**:
1. Verify Output Flywheel pipelines are running
2. Check for pipeline errors
3. Review work session creation

**Fix**: Trigger artifact creation or fix pipeline issues

---

## 📚 Related Documentation

- `systems/output_flywheel/README_METRICS.md` - Metrics system overview
- `systems/output_flywheel/METRICS_IMPLEMENTATION_SUMMARY.md` - Implementation details
- `money_ops/shipping_rhythm.yaml` - Shipping rhythm targets

---

## 🎯 Success Criteria

Guardrail system is successful when:
- ✅ Agents respond to YELLOW/RED status within SLA
- ✅ System health improves over time
- ✅ Artifacts are created and published consistently
- ✅ Captain receives timely alerts for issues

---

🐝 **WE. ARE. SWARM. ⚡🔥**

