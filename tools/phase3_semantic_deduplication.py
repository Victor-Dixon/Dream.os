#!/usr/bin/env python3
"""
Phase 3 Semantic Deduplication - Advanced Content Analysis
=========================================================

Intelligent deduplication using content analysis beyond simple hashing.
Identifies semantically similar files for consolidation.

Author: Agent-5 (Business Intelligence)
Date: 2026-01-11
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
from difflib import SequenceMatcher
import re

class SemanticDeduplicator:
    """Advanced semantic deduplication using content analysis."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.content_cache = {}
        self.semantic_groups = defaultdict(list)

    def load_sample_content(self, limit: int = 200) -> Dict[str, str]:
        """Load a sample of markdown content for analysis."""
        content = {}

        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
            for file in files:
                if file.endswith('.md') and len(content) < limit:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content[file_path] = f.read()
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

        return content

    def extract_semantic_features(self, content: str) -> Dict[str, any]:
        """Extract semantic features from content for similarity analysis."""
        features = {}

        # Extract headings
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        features['headings'] = [h.strip().lower() for h in headings[:5]]  # Top 5 headings

        # Extract key technical terms
        tech_terms = []
        tech_patterns = [
            r'\b(agent-\d+)\b',
            r'\b(phase\s+\d+)\b',
            r'\b(component|module|service|api)\b',
            r'\b(deployment|configuration|infrastructure)\b',
            r'\b(analytics|tracking|metrics)\b',
            r'\b(error|exception|debug|logging)\b'
        ]

        for pattern in tech_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            tech_terms.extend(matches)

        features['tech_terms'] = list(set(tech_terms))[:10]  # Top 10 unique terms

        # Extract structural elements
        features['has_code_blocks'] = '```' in content
        features['has_tables'] = '|' in content and re.search(r'\|.*\|.*\|', content)
        features['has_links'] = '[' in content and ']' in content
        features['line_count'] = len(content.split('\n'))

        return features

    def calculate_semantic_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calculate semantic similarity between two content feature sets."""
        similarity_score = 0.0

        # Heading similarity (30% weight)
        if features1['headings'] and features2['headings']:
            heading_sim = self._calculate_list_similarity(
                features1['headings'], features2['headings']
            )
            similarity_score += heading_sim * 0.3

        # Technical terms similarity (40% weight)
        if features1['tech_terms'] and features2['tech_terms']:
            term_sim = self._calculate_list_similarity(
                features1['tech_terms'], features2['tech_terms']
            )
            similarity_score += term_sim * 0.4

        # Structural similarity (20% weight)
        structural_features = ['has_code_blocks', 'has_tables', 'has_links']
        structural_matches = sum(
            1 for feat in structural_features
            if features1.get(feat) == features2.get(feat)
        )
        structural_sim = structural_matches / len(structural_features)
        similarity_score += structural_sim * 0.2

        # Size similarity (10% weight)
        size1, size2 = features1['line_count'], features2['line_count']
        if max(size1, size2) > 0:
            size_sim = 1 - abs(size1 - size2) / max(size1, size2)
            similarity_score += max(0, size_sim) * 0.1

        return min(similarity_score, 1.0)

    def _calculate_list_similarity(self, list1: List[str], list2: List[str]) -> float:
        """Calculate similarity between two lists."""
        if not list1 or not list2:
            return 0.0

        # Exact matches
        exact_matches = len(set(list1) & set(list2))
        total_unique = len(set(list1) | set(list2))

        if total_unique == 0:
            return 0.0

        return exact_matches / total_unique

    def find_semantic_duplicates(self, content_dict: Dict[str, str],
                               similarity_threshold: float = 0.7) -> List[Dict]:
        """Find semantically similar files using advanced analysis."""
        print(f"🔍 Analyzing {len(content_dict)} files for semantic duplicates...")

        # Extract features for all files
        file_features = {}
        for file_path, content in content_dict.items():
            file_features[file_path] = self.extract_semantic_features(content)

        semantic_groups = []
        processed = set()

        for file1, features1 in file_features.items():
            if file1 in processed:
                continue

            group = {
                'canonical_file': file1,
                'similar_files': [],
                'similarity_scores': [],
                'avg_similarity': 0.0,
                'confidence': 'low'
            }

            for file2, features2 in file_features.items():
                if file2 in processed or file2 == file1:
                    continue

                similarity = self.calculate_semantic_similarity(features1, features2)

                if similarity >= similarity_threshold:
                    group['similar_files'].append(file2)
                    group['similarity_scores'].append(similarity)

            if group['similar_files']:
                if group['similarity_scores']:
                    group['avg_similarity'] = sum(group['similarity_scores']) / len(group['similarity_scores'])

                    # Determine confidence level
                    if group['avg_similarity'] >= 0.85:
                        group['confidence'] = 'high'
                    elif group['avg_similarity'] >= 0.75:
                        group['confidence'] = 'medium'
                    else:
                        group['confidence'] = 'low'

                semantic_groups.append(group)
                processed.add(file1)
                processed.update(group['similar_files'])

                print(f"  📋 Found {group['confidence']} confidence group: "
                      f"{len(group['similar_files']) + 1} files "
                      f"(avg similarity: {group['avg_similarity']:.2f})")

        return semantic_groups

    def generate_deduplication_recommendations(self, semantic_groups: List[Dict]) -> Dict[str, any]:
        """Generate deduplication recommendations with risk assessment."""
        recommendations = {
            'high_confidence_actions': [],
            'medium_confidence_review': [],
            'low_confidence_manual': [],
            'summary': {
                'total_groups': len(semantic_groups),
                'high_confidence': len([g for g in semantic_groups if g['confidence'] == 'high']),
                'medium_confidence': len([g for g in semantic_groups if g['confidence'] == 'medium']),
                'low_confidence': len([g for g in semantic_groups if g['confidence'] == 'low']),
                'potential_savings': sum(len(g['similar_files']) for g in semantic_groups)
            }
        }

        for group in semantic_groups:
            action = {
                'canonical_file': group['canonical_file'],
                'similar_files': group['similar_files'],
                'avg_similarity': group['avg_similarity'],
                'file_count': len(group['similar_files']) + 1
            }

            if group['confidence'] == 'high':
                recommendations['high_confidence_actions'].append(action)
            elif group['confidence'] == 'medium':
                recommendations['medium_confidence_review'].append(action)
            else:
                recommendations['low_confidence_manual'].append(action)

        return recommendations

def main():
    """Main execution function."""
    print("🚀 Phase 3: Semantic Deduplication Analysis")
    print("=" * 50)

    repo_root = Path('.')
    deduplicator = SemanticDeduplicator(repo_root)

    # Load sample content
    print("Loading markdown content sample...")
    content_dict = deduplicator.load_sample_content(limit=100)

    print(f"Loaded {len(content_dict)} files for semantic analysis")

    # Find semantic duplicates
    semantic_groups = deduplicator.find_semantic_duplicates(
        content_dict, similarity_threshold=0.7
    )

    # Generate recommendations
    recommendations = deduplicator.generate_deduplication_recommendations(semantic_groups)

    # Save results
    import json
    results_file = 'reports/phase3_semantic_deduplication_results.json'
    with open(results_file, 'w') as f:
        json.dump(recommendations, f, indent=2, default=str)

    print("\n📊 Phase 3 Semantic Deduplication Results:")
    print(f"   Files analyzed: {len(content_dict)}")
    print(f"   Semantic groups found: {recommendations['summary']['total_groups']}")
    print(f"   High confidence: {recommendations['summary']['high_confidence']}")
    print(f"   Medium confidence: {recommendations['summary']['medium_confidence']}")
    print(f"   Low confidence: {recommendations['summary']['low_confidence']}")
    print(f"   Potential savings: {recommendations['summary']['potential_savings']} files")

    print(f"\n📄 Detailed results saved to: {results_file}")

    # Generate summary report
    summary_file = 'reports/phase3_semantic_deduplication_summary.md'
    with open(summary_file, 'w') as f:
        f.write(f"""# Phase 3 Semantic Deduplication Summary Report
**Generated:** 2026-01-11
**Agent:** Agent-5 (Business Intelligence)

## Executive Summary

**Analysis Results:**
- Files analyzed: {len(content_dict)}
- Semantic duplicate groups identified: {recommendations['summary']['total_groups']}
- High confidence actions: {recommendations['summary']['high_confidence']}
- Medium confidence reviews: {recommendations['summary']['medium_confidence']}
- Low confidence manual reviews: {recommendations['summary']['low_confidence']}
- Potential file savings: {recommendations['summary']['potential_savings']}

## Methodology

**Semantic Analysis Techniques:**
1. **Structural Feature Extraction:** Headings, technical terms, content structure
2. **Similarity Scoring:** Weighted algorithm (30% headings, 40% tech terms, 20% structure, 10% size)
3. **Confidence Classification:** High (≥85%), Medium (75-84%), Low (<75%)

## Recommendations

### High Confidence Actions ({len(recommendations['high_confidence_actions'])} groups)
Automated consolidation candidates with high similarity scores.

### Medium Confidence Reviews ({len(recommendations['medium_confidence_review'])} groups)
Require human review before consolidation.

### Low Confidence Manual Reviews ({len(recommendations['low_confidence_manual'])} groups)
Manual analysis recommended - similarity may not indicate true duplicates.

## Implementation Strategy

### Phase 3A: High Confidence Automation
Execute automated consolidation for high-confidence groups with rollback capability.

### Phase 3B: Medium Confidence Review
Human-supervised consolidation with detailed similarity analysis.

### Phase 3C: Low Confidence Assessment
Manual review for business value vs consolidation risk assessment.

## Risk Mitigation

- **Backup Creation:** All files backed up before consolidation
- **Rollback Capability:** Automated restoration scripts
- **Gradual Implementation:** Phase-wise execution with validation
- **Quality Assurance:** Content integrity verification post-consolidation

## Success Metrics

- **Storage Optimization:** Measure actual disk space recovered
- **Access Performance:** Monitor file access speed improvements
- **Maintenance Reduction:** Track time saved in file management
- **Content Quality:** Ensure no information loss in consolidation

**Phase 3 semantic deduplication analysis complete. Ready for implementation.**
""")

    print(f"📋 Summary report saved to: {summary_file}")

if __name__ == "__main__":
    main()