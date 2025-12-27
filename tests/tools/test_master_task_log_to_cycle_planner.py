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


