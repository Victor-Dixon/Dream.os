#!/usr/bin/env python3
"""Generate archive age manifest"""

import os
import csv
from datetime import datetime

def analyze_archive():
    """Analyze archive directory for age and size"""
    results = []

    if not os.path.exists('archive'):
        print("Archive directory not found")
        return results

    for root, dirs, files in os.walk('archive'):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                stat = os.stat(filepath)
                mtime = datetime.fromtimestamp(stat.st_mtime)
                age_days = (datetime.now() - mtime).days
                results.append({
                    'path': filepath,
                    'size': stat.st_size,
                    'modified': mtime.isoformat(),
                    'age_days': age_days,
                    'age_category': 'keep' if age_days < 30 else 'review' if age_days < 90 else 'compress' if age_days < 180 else 'archive'
                })
            except Exception as e:
                print(f"Error analyzing {filepath}: {e}")

    return results

if __name__ == "__main__":
    archive_data = analyze_archive()
    with open('audit_outputs/archive_age_manifest.csv', 'w', newline='') as f:
        if archive_data:
            writer = csv.DictWriter(f, fieldnames=['path', 'size', 'modified', 'age_days', 'age_category'])
            writer.writeheader()
            writer.writerows(archive_data)
        else:
            f.write("path,size,modified,age_days,age_category\n")
            f.write("archive/,,no_files_found,0,no_data\n")

    print(f"Generated archive manifest: {len(archive_data)} files analyzed")

    # Summary by category
    categories = {}
    for item in archive_data:
        cat = item['age_category']
        categories[cat] = categories.get(cat, 0) + 1

    print("Archive summary by retention category:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} files")