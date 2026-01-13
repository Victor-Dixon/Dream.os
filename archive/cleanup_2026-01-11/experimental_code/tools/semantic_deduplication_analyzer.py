#!/usr/bin/env python3
"""
Semantic Deduplication Analyzer - Phase 3 Markdown Cleanup
=========================================================

Advanced semantic analysis for markdown file deduplication beyond hash comparison.
Uses NLP techniques to identify conceptually similar content.

Author: Agent-5 (Business Intelligence)
Date: 2026-01-11
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import hashlib

@dataclass
class SemanticSimilarity:
    """Represents semantic similarity between two files."""
    file1: str
    file2: str
    similarity_score: float
    shared_keywords: Set[str]
    content_overlap: float

@dataclass
class DuplicateCluster:
    """Represents a cluster of semantically similar files."""
    files: List[str]
    cluster_type: str
    confidence: float
    shared_patterns: Dict[str, any]

class SemanticDeduplicationAnalyzer:
    """Advanced semantic analysis for markdown deduplication."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.content_cache = {}
        self.keyword_cache = {}

    def load_markdown_content(self, limit: int = None) -> Dict[str, str]:
        """Load markdown content with optional limit for testing."""
        content = {}
        count = 0

        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
            for file in files:
                if file.endswith('.md'):
                    if limit and count >= limit:
                        break
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content[file_path] = f.read()
                            count += 1
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
            if limit and count >= limit:
                break

        return content

    def extract_structural_keywords(self, content: str) -> Set[str]:
        """Extract structural keywords that indicate file type and purpose."""
        keywords = set()

        # Extract headers
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        keywords.update([h.strip().lower() for h in headers])

        # Extract key phrases and technical terms
        lines = content.split('\n')
        for line in lines[:50]:  # Focus on first 50 lines
            line = line.strip().lower()

            # Extract technical keywords
            tech_patterns = [
                r'\b(agent-\d+)\b',  # Agent references
                r'\b(phase\s+\d+)\b',  # Phase references
                r'\b(component|module|service|api)\b',  # Architecture terms
                r'\b(deployment|configuration|infrastructure)\b',  # DevOps terms
                r'\b(analytics|tracking|metrics|reporting)\b',  # BI terms
                r'\b(error|exception|debug|logging)\b',  # Development terms
                r'\b(task|workflow|pipeline|automation)\b',  # Process terms
            ]

            for pattern in tech_patterns:
                matches = re.findall(pattern, line)
                keywords.update(matches)

        return keywords

    def calculate_content_overlap(self, content1: str, content2: str) -> float:
        """Calculate content overlap using n-gram similarity."""
        def get_ngrams(text: str, n: int = 3) -> Set[str]:
            words = re.findall(r'\b\w+\b', text.lower())
            return set(' '.join(words[i:i+n]) for i in range(len(words)-n+1))

        ngrams1 = get_ngrams(content1, 3)
        ngrams2 = get_ngrams(content2, 3)

        if not ngrams1 or not ngrams2:
            return 0.0

        intersection = ngrams1 & ngrams2
        union = ngrams1 | ngrams2

        return len(intersection) / len(union) if union else 0.0

    def find_semantic_duplicates(self, content_dict: Dict[str, str],
                               min_similarity: float = 0.7) -> List[DuplicateCluster]:
        """Find semantically similar files using multiple similarity metrics."""
        files = list(content_dict.keys())
        clusters = []
        processed = set()

        print(f"Analyzing {len(files)} files for semantic duplicates...")

        for i, file1 in enumerate(files):
            if file1 in processed:
                continue

            cluster_files = [file1]
            cluster_keywords = self.extract_structural_keywords(content_dict[file1])
            cluster_similarities = []

            for j, file2 in enumerate(files[i+1:], i+1):
                if file2 in processed:
                    continue

                # Calculate multiple similarity metrics
                content_sim = self.calculate_content_overlap(
                    content_dict[file1], content_dict[file2]
                )

                keywords1 = self.extract_structural_keywords(content_dict[file1])
                keywords2 = self.extract_structural_keywords(content_dict[file2])
                keyword_sim = len(keywords1 & keywords2) / len(keywords1 | keywords2) if (keywords1 | keywords2) else 0.0

                # Weighted similarity score
                overall_sim = (content_sim * 0.7) + (keyword_sim * 0.3)

                if overall_sim >= min_similarity:
                    cluster_files.append(file2)
                    cluster_keywords.update(keywords2)
                    cluster_similarities.append(overall_sim)

            if len(cluster_files) > 1:
                # Determine cluster type
                cluster_type = self.classify_cluster(cluster_keywords, cluster_files)

                # Calculate confidence based on similarity consistency
                avg_similarity = sum(cluster_similarities) / len(cluster_similarities) if cluster_similarities else 0.0
                confidence = min(avg_similarity * 100, 95.0)  # Cap at 95%

                cluster = DuplicateCluster(
                    files=cluster_files,
                    cluster_type=cluster_type,
                    confidence=confidence,
                    shared_patterns={
                        'keywords': list(cluster_keywords),
                        'avg_similarity': avg_similarity,
                        'file_count': len(cluster_files)
                    }
                )

                clusters.append(cluster)
                processed.update(cluster_files)

                print(f"  Found {cluster_type} cluster: {len(cluster_files)} files (confidence: {confidence:.1f}%)")

        return clusters

    def classify_cluster(self, keywords: Set[str], files: List[str]) -> str:
        """Classify the type of duplicate cluster based on keywords and file patterns."""
        file_names = [os.path.basename(f) for f in files]

        # Check for devlog patterns
        if any('devlog' in name.lower() for name in file_names):
            return "devlog_duplicates"

        # Check for session closure patterns
        if any('session' in name.lower() and 'closure' in name.lower() for name in file_names):
            return "session_closure_duplicates"

        # Check for agent workspace patterns
        agent_patterns = ['agent-1', 'agent-2', 'agent-3', 'agent-4', 'agent-5', 'agent-7', 'agent-8']
        if any(any(pattern in f.lower() for pattern in agent_patterns) for f in files):
            return "agent_workspace_duplicates"

        # Check for archive patterns
        if any('archive' in f.lower() or 'backup' in f.lower() for f in files):
            return "archive_duplicates"

        # Check for documentation patterns
        doc_keywords = ['readme', 'documentation', 'guide', 'manual', 'reference']
        if any(any(kw in f.lower() for kw in doc_keywords) for f in files):
            return "documentation_duplicates"

        # Check for report patterns
        if any('report' in name.lower() for name in file_names):
            return "report_duplicates"

        return "general_duplicates"

    def generate_deduplication_report(self, clusters: List[DuplicateCluster]) -> str:
        """Generate comprehensive deduplication report."""
        total_files = sum(len(c.files) for c in clusters)
        potential_savings = sum(len(c.files) - 1 for c in clusters)

        report = f"""# Phase 3: Semantic Deduplication Analysis Report
**Generated:** 2026-01-11
**Agent:** Agent-5 (Business Intelligence)
**Analysis Method:** Advanced semantic similarity with NLP techniques

## Executive Summary

**Semantic Analysis Results:**
- Files analyzed: {len(self.content_cache)}
- Duplicate clusters identified: {len(clusters)}
- Files in duplicate clusters: {total_files}
- Potential space savings: {potential_savings} files ({potential_savings/total_files*100:.1f}% of duplicates)

**Analysis Methodology:**
- Content overlap using 3-gram similarity
- Structural keyword extraction and comparison
- Weighted similarity scoring (70% content, 30% keywords)
- Cluster classification by content type and patterns

## Cluster Analysis by Type

"""

        # Group clusters by type
        type_groups = defaultdict(list)
        for cluster in clusters:
            type_groups[cluster.cluster_type].append(cluster)

        for cluster_type, type_clusters in type_groups.items():
            total_files_in_type = sum(len(c.files) for c in type_clusters)
            avg_confidence = sum(c.confidence for c in type_clusters) / len(type_clusters)

            report += f"### {cluster_type.replace('_', ' ').title()} ({len(type_clusters)} clusters)\n"
            report += f"- Total files: {total_files_in_type}\n"
            report += f"- Average confidence: {avg_confidence:.1f}%\n"
            report += f"- Potential savings: {sum(len(c.files) - 1 for c in type_clusters)} files\n\n"

        report += "## High-Confidence Clusters (Confidence > 85%)\n\n"

        high_conf_clusters = [c for c in clusters if c.confidence > 85.0]
        for i, cluster in enumerate(high_conf_clusters[:20]):  # Show top 20
            report += f"### Cluster {i+1}: {cluster.cluster_type.replace('_', ' ').title()}\n"
            report += f"**Confidence:** {cluster.confidence:.1f}%\n"
            report += f"**Files:** {len(cluster.files)}\n"
            report += "**File list:**\n"
            for file_path in cluster.files[:10]:  # Show first 10 files
                report += f"- {file_path}\n"
            if len(cluster.files) > 10:
                report += f"- ... and {len(cluster.files) - 10} more\n"
            report += "\n"

        report += f"""
## Implementation Recommendations

### Phase 3A: High-Confidence Deduplication (Safe)
**Target:** {len(high_conf_clusters)} clusters with >85% confidence
**Risk Level:** Low
**Method:** Automated consolidation with human verification
**Estimated Savings:** {sum(len(c.files) - 1 for c in high_conf_clusters)} files

### Phase 3B: Medium-Confidence Review (Manual)
**Target:** {len([c for c in clusters if 70 <= c.confidence <= 85])} clusters with 70-85% confidence
**Risk Level:** Medium
**Method:** Human review with AI-assisted recommendations
**Estimated Savings:** {sum(len(c.files) - 1 for c in clusters if 70 <= c.confidence <= 85)} files

### Phase 3C: Low-Confidence Analysis (Optional)
**Target:** {len([c for c in clusters if c.confidence < 70])} clusters with <70% confidence
**Risk Level:** High
**Method:** Manual content analysis only
**Estimated Savings:** {sum(len(c.files) - 1 for c in clusters if c.confidence < 70])} files

## Technical Implementation

### Similarity Metrics Used
1. **Content Overlap:** 3-gram analysis for structural similarity
2. **Keyword Similarity:** Technical term and header comparison
3. **Weighted Scoring:** 70% content + 30% keyword similarity

### Cluster Classification Logic
- **Devlog Duplicates:** Files with 'devlog' in filename
- **Session Closures:** Files with 'session' and 'closure' patterns
- **Agent Workspaces:** Files containing agent identifiers
- **Archive Duplicates:** Files in archive/backup directories
- **Documentation:** Files with documentation keywords
- **Reports:** Files with 'report' in filename

## Next Steps

1. **Execute Phase 3A:** Automated high-confidence deduplication
2. **Review Phase 3B:** Manual verification of medium-confidence clusters
3. **Assess Phase 3C:** Evaluate business value vs. risk for low-confidence clusters
4. **Implement Automation:** Create recurring deduplication workflows
5. **Monitor Effectiveness:** Track storage savings and access patterns

## Risk Mitigation

### Automated Safeguards
- Confidence thresholds prevent false positives
- File modification time preservation
- Backup creation before consolidation
- Symlink creation instead of deletion (where possible)

### Manual Oversight
- Human review for medium-confidence clusters
- Business impact assessment for large consolidations
- Gradual rollout with rollback capabilities

### Quality Assurance
- Content integrity verification after consolidation
- Link validation for redirected references
- Performance impact monitoring

**Recommended Start:** Phase 3A automated deduplication within 24 hours.
"""
"""

        return report

def main():
    """Main execution function."""
    repo_root = Path('.')
    analyzer = SemanticDeduplicationAnalyzer(repo_root)

    print("🚀 Phase 3: Semantic Deduplication Analysis")
    print("=" * 50)

    # Load sample content for analysis (limit for performance)
    print("Loading markdown content...")
    content_dict = analyzer.load_markdown_content(limit=500)  # Analyze first 500 files

    print(f"Loaded {len(content_dict)} files for semantic analysis")

    # Find semantic duplicates
    clusters = analyzer.find_semantic_duplicates(content_dict, min_similarity=0.7)

    # Generate comprehensive report
    report = analyzer.generate_deduplication_report(clusters)

    # Save report
    report_path = Path('reports/semantic_deduplication_analysis_20260111.md')
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 Report saved to: reports/semantic_deduplication_analysis_20260111.md")
    print(f"📊 Analysis Complete:")
    print(f"   Files analyzed: {len(content_dict)}")
    print(f"   Duplicate clusters: {len(clusters)}")
    print(f"   Total duplicate files: {sum(len(c.files) for c in clusters)}")
    print(f"   Potential savings: {sum(len(c.files) - 1 for c in clusters)} files")

if __name__ == "__main__":
    main()