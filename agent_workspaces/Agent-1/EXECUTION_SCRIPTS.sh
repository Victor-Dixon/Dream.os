#!/bin/bash
# Agent-1 Consolidation Execution Scripts
# Execute when GitHub API rate limit resets

echo "🚀 Agent-1 Consolidation Execution"
echo "=================================="
echo ""

# Phase 2: Trading Repos
echo "📦 Phase 2: Trading Repos Consolidation"
echo "----------------------------------------"

echo "1. Merging trade-analyzer → trading-leads-bot"
python tools/repo_safe_merge.py trading-leads-bot trade-analyzer

echo ""
echo "2. Merging UltimateOptionsTradingRobot → trading-leads-bot"
python tools/repo_safe_merge.py trading-leads-bot UltimateOptionsTradingRobot

echo ""
echo "✅ Phase 2 Complete"
echo ""

# Phase 3: Agent Systems
echo "📦 Phase 3: Agent Systems Consolidation"
echo "----------------------------------------"

echo "1. Merging intelligent-multi-agent → Agent_Cellphone"
python tools/repo_safe_merge.py Agent_Cellphone intelligent-multi-agent

echo ""
echo "2. Archiving Agent_Cellphone_V1"
gh repo archive Dadudekc/Agent_Cellphone_V1 --yes

echo ""
echo "✅ Phase 3 Complete"
echo ""

echo "🎉 All Consolidation Complete!"
echo "Total: 4 repos consolidated"

