#!/usr/bin/env python3
"""
Distributes missing SSOT tag tasks to all 7 agents.
Divides the list of missing files into batches.

<!-- SSOT Domain: tools -->
"""

import os
from pathlib import Path
import json
import subprocess

def distribute_tasks():
    list_path = Path("agent_workspaces/Agent-6/MISSING_SSOT_TAGS_LIST.txt")
    if not list_path.exists():
        print("Missing tags list not found!")
        return
        
    files = list_path.read_text(encoding='utf-8').splitlines()
    total_files = len(files)
    
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    num_agents = len(agents)
    batch_size = (total_files // num_agents) + 1
    
    batches = {}
    for i, agent in enumerate(agents):
        start = i * batch_size
        end = min((i + 1) * batch_size, total_files)
        batches[agent] = files[start:end]
        
    # Save batches for tracking
    with open("agent_workspaces/Agent-6/SSOT_TAGGING_BATCHES.json", "w", encoding='utf-8') as f:
        json.dump(batches, f, indent=2)
        
    print(f"Distributed {total_files} files into {num_agents} batches.")
    
    # Generate messages for each agent
    for agent, batch in batches.items():
        if not batch:
            continue
            
        message = f"""# 🚨 URGENT: SSOT Tagging Batch - {agent}

**Task**: Add SSOT tags to {len(batch)} files.
**Format**: Add `<!-- SSOT Domain: domain_name -->` to the top of each file.
**Target Files**:
{chr(10).join(batch[:10])}
... and {len(batch) - 10} more.

Full list for your batch is in `agent_workspaces/Agent-6/SSOT_TAGGING_BATCHES.json`.
Please claim this task and execute in your next cycle.
"""
        # Save message to a file for use with messaging_cli
        msg_file = Path(f"agent_workspaces/Agent-6/SSOT_MSG_{agent}.md")
        msg_file.write_text(message, encoding='utf-8')
        
        # Send message via messaging_cli
        if agent != "Agent-6":
            cmd = [
                "python", "-m", "src.services.messaging_cli",
                "-a", agent,
                "-m", f"SSOT Tagging Task: Please check your workspace for batch assignment. {len(batch)} files assigned."
            ]
            try:
                # Use subprocess to run the command
                subprocess.run(cmd, check=True)
                print(f"Sent message to {agent}")
            except Exception as e:
                print(f"Failed to send message to {agent}: {e}")
        else:
            print(f"Skipping self-message for Agent-6. Task assigned internally.")

if __name__ == "__main__":
    distribute_tasks()



