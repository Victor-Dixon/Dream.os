# Work Resume Generator Guide

## Overview

The **Work Resume Generator** creates comprehensive summaries of agent work that serve as "resumes" - detailed context showing what work has been completed, current state, and next actions. This is perfect for:

- **Swarm Pulse Messages**: Include work resume in pulse messages to show what's been accomplished
- **Resume Prompts**: Use when agents need to get back up to speed after inactivity
- **Coordination**: Share work context with other agents
- **Status Reporting**: Provide detailed progress summaries

## Example Use Case

The Agent-6 swarm pulse message is a perfect example. It shows:
- ✅ Work completed (PR monitoring, coordination messages sent, status updates)
- 🔄 Current state (FSM state, tasks, coordination status)
- 📋 Next actions (clear, actionable steps)
- 🤝 Coordination activity (who you worked with, what messages were sent)

This comprehensive summary serves as a "work resume" that brings context and shows measurable progress.

## Usage

### Generate Work Resume via CLI

```bash
# Generate and display work resume for Agent-1
python -m src.services.messaging_cli --generate-work-resume --agent Agent-1

# Generate and save to file
python -m src.services.messaging_cli --generate-work-resume --agent Agent-1 --save-resume

# The resume will be saved to: agent_workspaces/Agent-1/WORK_RESUME_YYYYMMDD_HHMMSS.md
```

### Programmatic Usage

```python
from src.services.messaging.work_resume_generator import WorkResumeGenerator

generator = WorkResumeGenerator()

# Generate resume
resume = generator.generate_work_resume(
    agent_id="Agent-1",
    include_recent_commits=True,
    include_coordination=True,
    include_devlogs=True,
    days_back=7,
)

# Save to file
output_file = generator.save_resume_to_file("Agent-1")
```

## Resume Sections

The generated resume includes:

1. **Header**: Agent name, last updated, generation timestamp
2. **Current State**: FSM state, mission, phase, availability, coordination status, points
3. **Recent Work Completed**: List of completed tasks from status.json
4. **Current Tasks**: Active tasks with status, coordination info, and next actions
5. **Recent Commits**: Git commits (when git integration is added)
6. **Coordination Activity**: A2A messages sent/received (when message log integration is added)
7. **Recent Devlog Entries**: Summary of recent devlog files
8. **Next Actions**: Prioritized list of next actions
9. **Footer**: Use case and next steps

## Integration with Swarm Pulse

To include work resume in swarm pulse messages, modify the resume prompt generator:

```python
# In optimized_stall_resume_prompt.py or similar
from src.services.messaging.work_resume_generator import WorkResumeGenerator

# Generate resume
generator = WorkResumeGenerator()
work_resume = generator.generate_work_resume(agent_id)

# Append to swarm pulse message
pulse_message += "\n\n## 📋 YOUR WORK RESUME\n\n"
pulse_message += work_resume
```

## Future Enhancements

### Git Integration
- Read recent git commits for the agent
- Show commit messages, authors, dates
- Link commits to tasks/completed work

### Message Queue Integration
- Track A2A coordination messages sent/received
- Show coordination patterns and frequency
- Include message IDs and timestamps

### Activity Tracking
- Track file modifications
- Monitor test runs
- Log system utilization (Swarm Brain searches, contract claims, etc.)

### Status.json Updates
- Automatically update status.json with resume generation
- Track when resumes are generated
- Link resumes to activity cycles

## Best Practices

1. **Generate Regularly**: Generate work resumes as part of swarm pulse or status updates
2. **Include in Coordination**: Share work resume when coordinating with other agents
3. **Save for History**: Use `--save-resume` to maintain a history of work summaries
4. **Update Status.json**: Keep status.json current so resumes are accurate
5. **Use Devlogs**: Write devlogs consistently so they appear in work resumes

## Example Output

```
# 📋 WORK RESUME - Agent-6

**Agent**: Coordination & Communication Specialist  
**Last Updated**: 2025-12-21T17:30:00.000000Z  
**Generated**: 2025-12-21T17:44:04.629632  

## 🔄 CURRENT STATE
- **FSM State**: ACTIVE
- **Current Mission**: Infrastructure & DevOps Excellence
- **Current Phase**: Task Execution
...

## ✅ RECENT WORK COMPLETED
- PR monitoring updated - 5/7 PRs merged (71%)
- Coordination message sent to Agent-1
- Status.json updated with sync completion
- Devlog entry created
...

## 📋 CURRENT TASKS
- **PR Merge Status Monitoring** (ACTIVE)
  - Status: in_progress
  - Next: Monitor Agent-1 response, continue PR monitoring
...
```

## Related Files

- `src/services/messaging/work_resume_generator.py` - Main generator implementation
- `src/core/optimized_stall_resume_prompt.py` - Resume prompt generator (can integrate work resume)
- `src/core/messaging_template_texts.py` - SWARM_PULSE template (can include work resume)
- `agent_workspaces/{Agent-X}/status.json` - Source data for resume generation


