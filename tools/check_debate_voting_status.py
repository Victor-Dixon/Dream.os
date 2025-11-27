#!/usr/bin/env python3
"""
Check Tools Ranking Debate Voting Status
========================================

Checks which agents have voted for all 6 categories in the tools ranking debate.
"""

import json
from pathlib import Path
from collections import defaultdict

debate_file = Path("debates/debate_tools_ranking_20251124.json")

if not debate_file.exists():
    print(f"❌ Debate file not found: {debate_file}")
    exit(1)

with open(debate_file, encoding="utf-8") as f:
    debate_data = json.load(f)

# Get all 6 categories
categories = debate_data["options"]

# Count votes per agent from both "votes" dictionary and "arguments" array
agent_votes = defaultdict(set)

# Check "votes" dictionary
for vote_key, vote_data in debate_data["votes"].items():
    # Extract agent ID from vote key
    if "_" in vote_key:
        agent_id = vote_key.split("_")[0]
    else:
        agent_id = vote_key
    
    if agent_id.startswith("Agent-"):
        option = vote_data.get("option", "")
        agent_votes[agent_id].add(option)

# Also check "arguments" array (some agents may have voted there)
if "arguments" in debate_data:
    for arg in debate_data["arguments"]:
        agent_id = arg.get("agent_id", "")
        if agent_id.startswith("Agent-"):
            option = arg.get("option", "")
            agent_votes[agent_id].add(option)

# Check who has voted for all 6 categories
all_agents = [f"Agent-{i}" for i in range(1, 9)]
voted_all_6 = []
voted_partial = []
not_voted = []

for agent in all_agents:
    votes = agent_votes.get(agent, set())
    if len(votes) == 6:
        voted_all_6.append(agent)
    elif len(votes) > 0:
        voted_partial.append((agent, len(votes)))
    else:
        not_voted.append(agent)

print("=" * 60)
print("TOOLS RANKING DEBATE VOTING STATUS")
print("=" * 60)
print(f"\nDebate ID: {debate_data['debate_id']}")
print(f"Topic: {debate_data['topic']}")
print(f"Categories: {len(categories)}")
print(f"\nCategories:")
for i, cat in enumerate(categories, 1):
    print(f"  {i}. {cat}")

print("\n" + "=" * 60)
print("VOTING STATUS BY AGENT")
print("=" * 60)

print(f"\n✅ VOTED FOR ALL 6 CATEGORIES ({len(voted_all_6)}/8):")
for agent in voted_all_6:
    votes = agent_votes.get(agent, set())
    print(f"  ✅ {agent}: {len(votes)}/6 categories")

if voted_partial:
    print(f"\n⚠️  PARTIAL VOTES ({len(voted_partial)}/8):")
    for agent, count in voted_partial:
        votes = agent_votes.get(agent, set())
        missing = list(set(categories) - votes)
        missing_str = ', '.join(missing[:2]) if len(missing) > 2 else ', '.join(missing)
        print(f"  ⚠️  {agent}: {count}/6 categories (missing: {missing_str}...)")

if not_voted:
    print(f"\n❌ NOT VOTED ({len(not_voted)}/8):")
    for agent in not_voted:
        print(f"  ❌ {agent}: 0/6 categories")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Complete votes: {len(voted_all_6)}/8 ({len(voted_all_6)*100//8}%)")
print(f"  Partial votes: {len(voted_partial)}/8")
print(f"  Not voted: {len(not_voted)}/8")
print(f"  Total progress: {len(voted_all_6) + len(voted_partial)}/8 agents have voted")
print("=" * 60)

