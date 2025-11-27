#!/usr/bin/env python3
"""
Development Journey Analyzer - Chronological Blog Journey
==========================================================

Analyzes patterns, evolution, and progression across repos to identify:
- Skill progression over time
- Technology evolution
- Architectural patterns evolution
- Key milestones
- Development journey insights

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
Priority: HIGH
Mission: Chronological Blog Journey
"""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


def load_master_list() -> dict[str, Any]:
    """Load the master list of repos."""
    master_list_path = Path("data/github_75_repos_master_list.json")
    if not master_list_path.exists():
        raise FileNotFoundError(f"Master list not found: {master_list_path}")
    
    with open(master_list_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_chronology() -> Optional[dict[str, Any]]:
    """Load repository chronology data."""
    chronology_path = Path("data/repo_chronology.json")
    if not chronology_path.exists():
        return None
    
    with open(chronology_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_comprehensive_analysis() -> Optional[dict[str, Any]]:
    """Load comprehensive repo analysis data."""
    analysis_path = Path("agent_workspaces/Agent-5/comprehensive_repo_analysis_data.json")
    if not analysis_path.exists():
        return None
    
    with open(analysis_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_technology_evolution(chronology: Optional[dict[str, Any]], comprehensive: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Analyze technology stack evolution over time."""
    evolution = {
        "technologies_timeline": [],
        "technology_frequency": defaultdict(int),
        "new_technologies_introduced": [],
        "technology_trends": {},
    }
    
    if not chronology or not comprehensive:
        return evolution
    
    repo_data = comprehensive.get("repo_data", {})
    chronology_list = chronology.get("chronology", [])
    
    # Track technologies over time
    technologies_by_period = defaultdict(set)
    
    for repo_entry in chronology_list:
        repo_num = repo_entry.get("repo_num")
        created_at = repo_entry.get("created_at_iso")
        repo_name = repo_entry.get("name", "")
        
        if not created_at or not repo_num:
            continue
        
        # Get repo data
        repo_key = str(repo_num)
        repo_info = repo_data.get(repo_key, {})
        
        # Extract technologies (simplified - would need more detailed analysis)
        languages = repo_entry.get("language")
        if languages:
            if isinstance(languages, str):
                technologies_by_period[created_at[:7]].add(languages)  # Group by month
                evolution["technology_frequency"][languages] += 1
        
        # Try to get more tech info from repo_data
        tech_stack = repo_info.get("tech_stack", [])
        if tech_stack:
            for tech in tech_stack:
                technologies_by_period[created_at[:7]].add(tech)
                evolution["technology_frequency"][tech] += 1
    
    # Create timeline
    sorted_periods = sorted(technologies_by_period.keys())
    for period in sorted_periods:
        evolution["technologies_timeline"].append({
            "period": period,
            "technologies": sorted(list(technologies_by_period[period])),
            "count": len(technologies_by_period[period]),
        })
    
    # Identify trends
    tech_counts = dict(evolution["technology_frequency"])
    top_technologies = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    evolution["technology_trends"]["top_10_technologies"] = [
        {"technology": tech, "count": count} for tech, count in top_technologies
    ]
    
    return evolution


def analyze_skill_progression(chronology: Optional[dict[str, Any]], comprehensive: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Analyze skill progression over time."""
    progression = {
        "complexity_trends": [],
        "project_types_evolution": [],
        "skill_milestones": [],
        "learning_patterns": {},
    }
    
    if not chronology or not comprehensive:
        return progression
    
    repo_data = comprehensive.get("repo_data", {})
    chronology_list = chronology.get("chronology", [])
    
    # Track project complexity over time
    complexity_by_period = defaultdict(list)
    
    for repo_entry in chronology_list:
        repo_num = repo_entry.get("repo_num")
        created_at = repo_entry.get("created_at_iso")
        
        if not created_at or not repo_num:
            continue
        
        repo_key = str(repo_num)
        repo_info = repo_data.get(repo_key, {})
        
        # Estimate complexity (simplified - would need better metrics)
        size = repo_entry.get("size", 0)
        languages = repo_entry.get("language")
        
        complexity_score = 0
        if size:
            if size < 1000:
                complexity_score = 1
            elif size < 10000:
                complexity_score = 2
            else:
                complexity_score = 3
        
        period = created_at[:7]  # Group by month
        complexity_by_period[period].append({
            "repo_num": repo_num,
            "name": repo_entry.get("name", ""),
            "complexity": complexity_score,
            "size": size,
        })
    
    # Calculate average complexity per period
    sorted_periods = sorted(complexity_by_period.keys())
    for period in sorted_periods:
        repos_in_period = complexity_by_period[period]
        avg_complexity = sum(r["complexity"] for r in repos_in_period) / len(repos_in_period) if repos_in_period else 0
        
        progression["complexity_trends"].append({
            "period": period,
            "average_complexity": avg_complexity,
            "repo_count": len(repos_in_period),
            "repos": repos_in_period,
        })
    
    return progression


def analyze_architectural_patterns(chronology: Optional[dict[str, Any]], comprehensive: Optional[dict[str, Any]]) -> dict[str, Any]:
    """Analyze architectural patterns evolution."""
    patterns = {
        "pattern_timeline": [],
        "pattern_frequency": defaultdict(int),
        "architectural_evolution": [],
        "design_milestones": [],
    }
    
    if not chronology or not comprehensive:
        return patterns
    
    repo_data = comprehensive.get("repo_data", {})
    chronology_list = chronology.get("chronology", [])
    
    # Extract architectural patterns (would need more detailed analysis from repo data)
    # For now, infer from categories and names
    patterns_by_period = defaultdict(set)
    
    for repo_entry in chronology_list:
        repo_num = repo_entry.get("repo_num")
        created_at = repo_entry.get("created_at_iso")
        
        if not created_at or not repo_num:
            continue
        
        repo_key = str(repo_num)
        repo_info = repo_data.get(repo_key, {})
        repo_name = repo_entry.get("name", "").lower()
        
        # Infer patterns from names and categories
        inferred_patterns = []
        
        if "agent" in repo_name or "multi-agent" in repo_name.lower():
            inferred_patterns.append("multi-agent")
            patterns["pattern_frequency"]["multi-agent"] += 1
        
        if "api" in repo_name or "fastapi" in repo_name:
            inferred_patterns.append("api-driven")
            patterns["pattern_frequency"]["api-driven"] += 1
        
        if "bot" in repo_name or "discord" in repo_name:
            inferred_patterns.append("bot/automation")
            patterns["pattern_frequency"]["bot/automation"] += 1
        
        if "os" in repo_name:
            inferred_patterns.append("system-like")
            patterns["pattern_frequency"]["system-like"] += 1
        
        period = created_at[:7]
        for pattern in inferred_patterns:
            patterns_by_period[period].add(pattern)
    
    # Create timeline
    sorted_periods = sorted(patterns_by_period.keys())
    for period in sorted_periods:
        patterns["pattern_timeline"].append({
            "period": period,
            "patterns": sorted(list(patterns_by_period[period])),
            "pattern_count": len(patterns_by_period[period]),
        })
    
    return patterns


def identify_milestones(chronology: Optional[dict[str, Any]], comprehensive: Optional[dict[str, Any]]) -> list[dict[str, Any]]:
    """Identify key milestones in the development journey."""
    milestones = []
    
    if not chronology:
        return milestones
    
    chronology_list = chronology.get("chronology", [])
    
    # First repo
    if chronology_list:
        first_repo = chronology_list[0]
        milestones.append({
            "milestone_type": "journey_start",
            "repo_num": first_repo.get("repo_num"),
            "repo_name": first_repo.get("name", ""),
            "date": first_repo.get("created_at_iso", ""),
            "description": "First repository - Beginning of development journey",
        })
    
    # 25th repo (33% mark)
    if len(chronology_list) >= 25:
        repo_25 = chronology_list[24]
        milestones.append({
            "milestone_type": "one_third_complete",
            "repo_num": repo_25.get("repo_num"),
            "repo_name": repo_25.get("name", ""),
            "date": repo_25.get("created_at_iso", ""),
            "description": "25th repository - One-third of journey complete",
        })
    
    # 50th repo (67% mark)
    if len(chronology_list) >= 50:
        repo_50 = chronology_list[49]
        milestones.append({
            "milestone_type": "two_thirds_complete",
            "repo_num": repo_50.get("repo_num"),
            "repo_name": repo_50.get("name", ""),
            "date": repo_50.get("created_at_iso", ""),
            "description": "50th repository - Two-thirds of journey complete",
        })
    
    # Most recent repo
    if chronology_list:
        latest_repo = chronology_list[-1]
        milestones.append({
            "milestone_type": "current_state",
            "repo_num": latest_repo.get("repo_num"),
            "repo_name": latest_repo.get("name", ""),
            "date": latest_repo.get("created_at_iso", ""),
            "description": "Most recent repository - Current state of development",
        })
    
    # Year boundaries
    time_periods = chronology.get("time_periods", {})
    if time_periods.get("year_2", {}).get("start_date"):
        milestones.append({
            "milestone_type": "year_2_start",
            "date": time_periods["year_2"]["start_date"],
            "description": "Beginning of Year 2",
            "repo_count": time_periods["year_1"]["repo_count"],
        })
    
    if time_periods.get("year_3", {}).get("start_date"):
        milestones.append({
            "milestone_type": "year_3_start",
            "date": time_periods["year_3"]["start_date"],
            "description": "Beginning of Year 3",
            "repo_count": time_periods["year_1"]["repo_count"] + time_periods["year_2"]["repo_count"],
        })
    
    return milestones


def analyze_development_journey() -> dict[str, Any]:
    """Perform comprehensive development journey analysis."""
    print("Loading data sources...")
    master_list = load_master_list()
    chronology = load_chronology()
    comprehensive = load_comprehensive_analysis()
    
    if not chronology:
        print("⚠️  Warning: Chronology data not found. Run get_repo_chronology.py first.")
        print("   Analysis will proceed with limited data.")
    
    print("Analyzing technology evolution...")
    tech_evolution = analyze_technology_evolution(chronology, comprehensive)
    
    print("Analyzing skill progression...")
    skill_progression = analyze_skill_progression(chronology, comprehensive)
    
    print("Analyzing architectural patterns...")
    architectural_patterns = analyze_architectural_patterns(chronology, comprehensive)
    
    print("Identifying milestones...")
    milestones = identify_milestones(chronology, comprehensive)
    
    # Calculate journey statistics
    total_repos = len(master_list.get("repos", []))
    analyzed_repos = sum(1 for r in master_list.get("repos", []) if r.get("analyzed", False))
    
    journey_stats = {
        "total_repos": total_repos,
        "analyzed_repos": analyzed_repos,
        "analysis_coverage": (analyzed_repos / total_repos * 100) if total_repos > 0 else 0,
    }
    
    if chronology:
        time_periods = chronology.get("time_periods", {})
        journey_stats["year_1_repos"] = time_periods.get("year_1", {}).get("repo_count", 0)
        journey_stats["year_2_repos"] = time_periods.get("year_2", {}).get("repo_count", 0)
        journey_stats["year_3_repos"] = time_periods.get("year_3", {}).get("repo_count", 0)
    
    result = {
        "generated_at": datetime.now().isoformat(),
        "journey_statistics": journey_stats,
        "technology_evolution": tech_evolution,
        "skill_progression": skill_progression,
        "architectural_patterns": architectural_patterns,
        "milestones": milestones,
        "journey_insights": {
            "summary": "Development journey analysis showing evolution over 3 years",
            "key_findings": [
                f"Total repositories: {total_repos}",
                f"Analyzed: {analyzed_repos} ({journey_stats['analysis_coverage']:.1f}%)",
                f"Technologies used: {len(tech_evolution['technology_frequency'])}",
                f"Key milestones: {len(milestones)}",
            ],
        },
    }
    
    return result


def print_journey_report(analysis: dict[str, Any]) -> None:
    """Print development journey analysis report."""
    print("=" * 80)
    print("DEVELOPMENT JOURNEY ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    stats = analysis["journey_statistics"]
    print("JOURNEY STATISTICS:")
    print(f"  Total Repositories: {stats['total_repos']}")
    print(f"  Analyzed: {stats['analyzed_repos']} ({stats['analysis_coverage']:.1f}%)")
    
    if "year_1_repos" in stats:
        print(f"  Year 1 Repos: {stats['year_1_repos']}")
        print(f"  Year 2 Repos: {stats['year_2_repos']}")
        print(f"  Year 3 Repos: {stats['year_3_repos']}")
    print()
    
    tech_evolution = analysis["technology_evolution"]
    print("TECHNOLOGY EVOLUTION:")
    print(f"  Total Technologies: {len(tech_evolution['technology_frequency'])}")
    if tech_evolution["technology_trends"].get("top_10_technologies"):
        print("  Top Technologies:")
        for tech in tech_evolution["technology_trends"]["top_10_technologies"][:5]:
            print(f"    - {tech['technology']}: {tech['count']} repos")
    print()
    
    milestones = analysis["milestones"]
    print(f"MILESTONES IDENTIFIED: {len(milestones)}")
    for milestone in milestones:
        date = milestone.get("date", "Unknown")[:10] if milestone.get("date") else "Unknown"
        print(f"  - {milestone['milestone_type']}: {date}")
        if milestone.get("repo_name"):
            print(f"    Repo: {milestone['repo_name']}")
        print(f"    {milestone.get('description', '')}")
    print()
    
    insights = analysis["journey_insights"]
    print("KEY INSIGHTS:")
    for finding in insights.get("key_findings", []):
        print(f"  - {finding}")
    print()
    
    print("=" * 80)


def main():
    """Main execution."""
    print("=" * 80)
    print("DEVELOPMENT JOURNEY ANALYZER")
    print("=" * 80)
    print()
    
    try:
        analysis = analyze_development_journey()
        print_journey_report(analysis)
        
        # Save to file
        output_path = Path("data/development_journey_analysis.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Analysis saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Ensure required data files exist before running analysis.")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())


