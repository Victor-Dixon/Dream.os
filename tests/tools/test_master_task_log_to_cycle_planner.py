from pathlib import Path

import pytest


@pytest.mark.unit
def test_parse_master_task_log_extracts_agent_assigned_tasks(tmp_path: Path):
    content = """# MASTER TASK LOG

## 📥 INBOX

- [ ] **HIGH** (100 pts): Do thing A [Agent-3]
- [x] **MEDIUM** (50 pts): Done thing [Agent-3]
- [ ] **LOW** (10 pts): Do thing B [Agent-7]

## 🎯 THIS WEEK (Max 5 Items)

- [ ] **MEDIUM** (75 pts): Weekly task [Agent-3]
"""

    p = tmp_path / "MASTER_TASK_LOG.md"
    p.write_text(content, encoding="utf-8")

    from tools import master_task_log_to_cycle_planner as mtl2cp

    tasks = mtl2cp.parse_master_task_log(p)
    # Parser includes both checked and unchecked items; downstream filters handle checked.
    assert len(tasks) == 4
    assert {t.section for t in tasks} == {"INBOX", "THIS_WEEK"}

    inbox = [t for t in tasks if t.section == "INBOX"]
    payload = mtl2cp.build_cycle_planner_payload(agent_id="Agent-3", tasks=inbox, priority="high")
    assert payload["agent_id"] == "Agent-3"
    # build_cycle_planner_payload filters to unchecked + assigned Agent-3 tasks
    assert payload["total_tasks"] == 1
    assert payload["tasks"][0]["assigned_to"] == "Agent-3"
    assert "Do thing A" in payload["tasks"][0]["title"]


