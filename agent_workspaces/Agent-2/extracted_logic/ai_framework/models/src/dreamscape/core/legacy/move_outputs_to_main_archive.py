#!/usr/bin/env python3
"""
Move Outputs Archive and Backup to Main Archive

This script moves the outputs/archive and outputs/backup directories
to the main project archive directory where they belong.
"""

import shutil
from pathlib import Path
from datetime import datetime

def move_outputs_to_main_archive():
    """Move outputs archive and backup to main archive directory"""
    
    # Define paths
    outputs_dir = Path("outputs")
    main_archive_dir = Path("archive")
    
    print("Moving outputs archive and backup to main archive directory...")
    
    # Move outputs/archive to archive/outputs_archive
    outputs_archive = outputs_dir / "archive"
    main_outputs_archive = main_archive_dir / "outputs_archive"
    
    if outputs_archive.exists():
        if main_outputs_archive.exists():
            # If destination exists, merge contents
            print(f"Merging {outputs_archive} into {main_outputs_archive}...")
            for item in outputs_archive.iterdir():
                if item.is_file():
                    shutil.move(str(item), str(main_outputs_archive / item.name))
                elif item.is_dir():
                    dest_dir = main_outputs_archive / item.name
                    if dest_dir.exists():
                        # Merge subdirectories
                        for subitem in item.iterdir():
                            if subitem.is_file():
                                shutil.move(str(subitem), str(dest_dir / subitem.name))
                            elif subitem.is_dir():
                                shutil.move(str(subitem), str(dest_dir / subitem.name))
                    else:
                        shutil.move(str(item), str(main_outputs_archive / item.name))
            
            # Remove the now-empty outputs_archive directory
            shutil.rmtree(outputs_archive)
        else:
            # Move the entire directory
            shutil.move(str(outputs_archive), str(main_outputs_archive))
            print(f"Moved {outputs_archive} to {main_outputs_archive}")
    else:
        print(f"Outputs archive directory not found: {outputs_archive}")
    
    # Move outputs/backup to archive/backups/outputs_backup_YYYYMMDD_HHMMSS
    outputs_backup = outputs_dir / "backup"
    if outputs_backup.exists():
        # Find the most recent backup directory
        backup_dirs = list(outputs_backup.iterdir())
        if backup_dirs:
            # Get the most recent backup directory
            latest_backup = max(backup_dirs, key=lambda x: x.stat().st_mtime)
            
            # Create timestamp for the new backup location
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            main_backup_dir = main_archive_dir / "backups" / f"outputs_backup_{timestamp}"
            
            # Move the latest backup
            shutil.move(str(latest_backup), str(main_backup_dir))
            print(f"Moved outputs backup to {main_backup_dir}")
            
            # Remove the now-empty backup directory
            shutil.rmtree(outputs_backup)
        else:
            print("No backup directories found in outputs/backup")
    else:
        print(f"Outputs backup directory not found: {outputs_backup}")
    
    # Create a README in the main outputs_archive directory
    readme_path = main_archive_dir / "outputs_archive" / "README.md"
    if not readme_path.exists():
        readme_content = """# Outputs Archive

This directory contains archived files from the outputs directory organization.

## Contents

- **old_reports/**: Outdated consolidation and analysis reports
- **test_files/**: Test files and one-off scripts
- **examples/**: Example files and demos
- **uncategorized/**: Files that didn't fit other categories

## Organization Date

These files were organized and archived on: {date}

## Original Location

These files were originally in `outputs/` and were moved here during the organization process.
""".format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        readme_path.write_text(readme_content)
    
    print("Move complete!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Move outputs archive and backup to main archive")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved without doing it")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("DRY RUN MODE - Would move the following:")
        outputs_dir = Path("outputs")
        main_archive_dir = Path("archive")
        
        outputs_archive = outputs_dir / "archive"
        outputs_backup = outputs_dir / "backup"
        
        if outputs_archive.exists():
            print(f"  - {outputs_archive} -> {main_archive_dir}/outputs_archive")
        else:
            print(f"  - {outputs_archive} (not found)")
            
        if outputs_backup.exists():
            print(f"  - {outputs_backup} -> {main_archive_dir}/backups/outputs_backup_YYYYMMDD_HHMMSS")
        else:
            print(f"  - {outputs_backup} (not found)")
    else:
        move_outputs_to_main_archive()

if __name__ == "__main__":
    main() 