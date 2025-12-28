from pathlib import Path

import pytest


@pytest.mark.unit
def test_parse_master_task_log_extracts_agent_assigned_tasks(tmp_path: Path):
    # Create a minimal MASTER_TASK_LOG-like file
    content = """# MASTER TASK LOG

## 📥 INBOX

- [ ] **HIGH** (100 pts): Do thing A [Agent-3]
- [ ] **MEDIUM**: Do thing B [Agent-7]
- [x] **LOW**: Completed thing [Agent-3]

## 🎯 THIS WEEK (Max 5 Items)

- [ ] **CRITICAL** (150 pts): Do thing C [Agent-3]
"""
    log_path = tmp_path / "MASTER_TASK_LOG.md"
    log_path.write_text(content, encoding="utf-8")

    from tools import master_task_log_to_cycle_planner as mtl2cp

    tasks = mtl2cp.parse_master_task_log(log_path)
    assert any(t.section == "INBOX" for t in tasks)
    assert any(t.section == "THIS_WEEK" for t in tasks)

    # Ensure agent filter keeps only unchecked Agent-3 tasks
    inbox = [t for t in tasks if t.section == "INBOX"]
    payload = mtl2cp.build_cycle_planner_payload(agent_id="Agent-3", tasks=inbox, priority="high")
    assert payload["agent_id"] == "Agent-3"
    assert payload["total_tasks"] == 1
    assert payload["tasks"][0]["assigned_to"] == "Agent-3"
    assert "Do thing A" in payload["tasks"][0]["title"]

from pathlib import Path

import pytest


@pytest.mark.unit
def test_parse_master_task_log_extracts_agent_assigned_tasks(tmp_path: Path):
    from tools.master_task_log_to_cycle_planner import parse_master_task_log

    content = """# MASTER TASK LOG

## INBOX
- [ ] **HIGH** (100 pts): Do thing A [Agent-3]
- [x] **MEDIUM** (50 pts): Done thing [Agent-3]
- [ ] **LOW** (10 pts): Do thing B [Agent-7]

## THIS WEEK
- [ ] **MEDIUM** (75 pts): Weekly task [Agent-3]
"""

    p = tmp_path / "MASTER_TASK_LOG.md"
    p.write_text(content, encoding="utf-8")

    tasks = parse_master_task_log(p)
    # Unchecked tasks for Agent-3 and Agent-7 are included; checked items are excluded.
    assert len(tasks) == 3
    assert {t.section for t in tasks} == {"INBOX", "THIS_WEEK"}
    assert {t.assigned_agent for t in tasks} == {"Agent-3", "Agent-7"}


