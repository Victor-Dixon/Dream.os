#!/usr/bin/env python3
"""
Consolidate Remaining Duplicates
================================

Quick consolidation script to address the remaining 16 true duplicate issues:
- Context manager patterns (__enter__/__exit__)
- Database cleanup patterns (__del__)
- Simple utility patterns (__init__, __post_init__, close)
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.dreamscape.core.utils.print_utils import (
    print_header, print_section, print_step, print_success,
    print_info, print_warning, print_error
)

class RemainingDuplicateConsolidator:
    """Consolidate remaining duplicate patterns."""
    
    def __init__(self):
        self.project_root = project_root
        self.backup_dir = project_root / "backups" / "consolidation_backup"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Define consolidation patterns
        self.consolidation_patterns = {
            'context_manager_mixin': {
                'description': 'Context manager mixin for __enter__/__exit__ patterns',
                'target_file': 'src/dreamscape/core/utils/context_mixin.py',
                'content': '''"""
Context Manager Mixin
====================

Provides common context manager functionality for database and resource management.
"""

class ContextManagerMixin:
    """Mixin providing standard context manager functionality."""
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.close()
    
    def close(self):
        """Close the resource. Override in subclasses."""
        pass
'''
            },
            'database_cleanup_mixin': {
                'description': 'Database cleanup mixin for __del__ patterns',
                'target_file': 'src/dreamscape/core/utils/database_mixin.py',
                'content': '''"""
Database Cleanup Mixin
======================

Provides common database cleanup functionality.
"""

class DatabaseCleanupMixin:
    """Mixin providing standard database cleanup functionality."""
    
    def __del__(self):
        """Clean up database connection."""
        if hasattr(self, 'conn'):
            self.conn.close()
'''
            },
            'config_manager_mixin': {
                'description': 'Config manager mixin for __post_init__ patterns',
                'target_file': 'src/dreamscape/core/utils/config_mixin.py',
                'content': '''"""
Config Manager Mixin
====================

Provides common configuration management functionality.
"""

class ConfigManagerMixin:
    """Mixin providing standard configuration management functionality."""
    
    def __post_init__(self):
        """Post-initialization setup."""
        if hasattr(self, 'capabilities') and self.capabilities is None:
            self.capabilities = []
'''
            }
        }
        
        # Files to consolidate
        self.files_to_consolidate = {
            'context_manager_mixin': [
                'src/dreamscape/core/memory_manager.py',
                'src/dreamscape/core/memory_storage.py', 
                'src/dreamscape/core/resume_tracker.py',
                'src/dreamscape/core/scraper_orchestrator.py',
                'src/dreamscape/core/utils/core_utils.py',
                'src/dreamscape/core/memory_api.py',
                'src/dreamscape/core/resume_database.py'
            ],
            'database_cleanup_mixin': [
                'scripts/consolidate_template_analyzers.py',
                'src/dreamscape/core/context_manager.py',
                'src/dreamscape/core/template_engine.py',
                'src/dreamscape/core/utils/core_utils.py'
            ],
            'config_manager_mixin': [
                'src/dreamscape/core/agent_config_manager.py',
                'src/dreamscape/core/model_config_manager.py'
            ]
        }
    
    def create_mixin_files(self) -> None:
        """Create the mixin utility files."""
        print_header("Creating Mixin Utility Files")
        
        for mixin_name, mixin_info in self.consolidation_patterns.items():
            target_path = self.project_root / mixin_info['target_file']
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Backup if exists
            if target_path.exists():
                backup_path = self.backup_dir / f"{mixin_name}_backup.py"
                shutil.copy2(target_path, backup_path)
                print_info(f"Backed up existing {mixin_name} to {backup_path}")
            
            # Create mixin file
            target_path.write_text(mixin_info['content'], encoding='utf-8')
            print_success(f"Created {mixin_name}: {target_path}")
    
    def consolidate_context_managers(self) -> None:
        """Consolidate context manager patterns."""
        print_section("Consolidating Context Manager Patterns")
        
        mixin_import = "from src.dreamscape.core.utils.context_mixin import ContextManagerMixin"
        
        for file_path in self.files_to_consolidate['context_manager_mixin']:
            full_path = self.project_root / file_path
            if not full_path.exists():
                print_warning(f"File not found: {file_path}")
                continue
            
            try:
                # Backup file
                backup_path = self.backup_dir / f"{file_path.replace('/', '_')}_backup.py"
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(full_path, backup_path)
                
                # Read content
                content = full_path.read_text(encoding='utf-8')
                
                # Check if already has mixin
                if 'ContextManagerMixin' in content:
                    print_info(f"Already has mixin: {file_path}")
                    continue
                
                # Add mixin import
                if 'from src.dreamscape.core.utils' in content:
                    # Insert after existing dreamscape imports
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'from src.dreamscape.core.utils' in line:
                            lines.insert(i + 1, mixin_import)
                            break
                    else:
                        # Insert after other imports
                        for i, line in enumerate(lines):
                            if line.strip() and not line.startswith(('import ', 'from ')):
                                lines.insert(i, mixin_import)
                                break
                        else:
                            lines.insert(0, mixin_import)
                    content = '\n'.join(lines)
                
                # Replace __enter__ and __exit__ methods
                content = self._replace_context_methods(content)
                
                # Write back
                full_path.write_text(content, encoding='utf-8')
                print_success(f"Consolidated context manager: {file_path}")
                
            except Exception as e:
                print_error(f"Error consolidating {file_path}: {e}")
    
    def _replace_context_methods(self, content: str) -> str:
        """Replace __enter__ and __exit__ methods with mixin usage."""
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            # Check for class definition
            if line.strip().startswith('class ') and ':' in line:
                # Add mixin to class
                if 'ContextManagerMixin' not in line:
                    line = line.replace(':', '(ContextManagerMixin):')
                    new_lines.append(line)
                    continue
            
            # Skip __enter__ and __exit__ methods
            if any(method in line for method in ['def __enter__', 'def __exit__']):
                # Skip the method definition and its content
                skip_next = True
                indent = len(line) - len(line.lstrip())
                j = i + 1
                while j < len(lines) and (lines[j].strip() == '' or 
                                        len(lines[j]) - len(lines[j].lstrip()) > indent):
                    j += 1
                    skip_next = True
                continue
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def consolidate_database_cleanup(self) -> None:
        """Consolidate database cleanup patterns."""
        print_section("Consolidating Database Cleanup Patterns")
        
        mixin_import = "from src.dreamscape.core.utils.database_mixin import DatabaseCleanupMixin"
        
        for file_path in self.files_to_consolidate['database_cleanup_mixin']:
            full_path = self.project_root / file_path
            if not full_path.exists():
                print_warning(f"File not found: {file_path}")
                continue
            
            try:
                # Backup file
                backup_path = self.backup_dir / f"{file_path.replace('/', '_')}_backup.py"
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(full_path, backup_path)
                
                # Read content
                content = full_path.read_text(encoding='utf-8')
                
                # Check if already has mixin
                if 'DatabaseCleanupMixin' in content:
                    print_info(f"Already has mixin: {file_path}")
                    continue
                
                # Add mixin import
                if 'from src.dreamscape.core.utils' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'from src.dreamscape.core.utils' in line:
                            lines.insert(i + 1, mixin_import)
                            break
                    else:
                        lines.insert(0, mixin_import)
                    content = '\n'.join(lines)
                
                # Replace __del__ methods
                content = self._replace_del_methods(content)
                
                # Write back
                full_path.write_text(content, encoding='utf-8')
                print_success(f"Consolidated database cleanup: {file_path}")
                
            except Exception as e:
                print_error(f"Error consolidating {file_path}: {e}")
    
    def _replace_del_methods(self, content: str) -> str:
        """Replace __del__ methods with mixin usage."""
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            # Check for class definition
            if line.strip().startswith('class ') and ':' in line:
                # Add mixin to class
                if 'DatabaseCleanupMixin' not in line:
                    line = line.replace(':', '(DatabaseCleanupMixin):')
                    new_lines.append(line)
                    continue
            
            # Skip __del__ methods
            if 'def __del__' in line:
                # Skip the method definition and its content
                skip_next = True
                indent = len(line) - len(line.lstrip())
                j = i + 1
                while j < len(lines) and (lines[j].strip() == '' or 
                                        len(lines[j]) - len(lines[j].lstrip()) > indent):
                    j += 1
                    skip_next = True
                continue
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def consolidate_config_managers(self) -> None:
        """Consolidate config manager patterns."""
        print_section("Consolidating Config Manager Patterns")
        
        mixin_import = "from src.dreamscape.core.utils.config_mixin import ConfigManagerMixin"
        
        for file_path in self.files_to_consolidate['config_manager_mixin']:
            full_path = self.project_root / file_path
            if not full_path.exists():
                print_warning(f"File not found: {file_path}")
                continue
            
            try:
                # Backup file
                backup_path = self.backup_dir / f"{file_path.replace('/', '_')}_backup.py"
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(full_path, backup_path)
                
                # Read content
                content = full_path.read_text(encoding='utf-8')
                
                # Check if already has mixin
                if 'ConfigManagerMixin' in content:
                    print_info(f"Already has mixin: {file_path}")
                    continue
                
                # Add mixin import
                if 'from src.dreamscape.core.utils' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'from src.dreamscape.core.utils' in line:
                            lines.insert(i + 1, mixin_import)
                            break
                    else:
                        lines.insert(0, mixin_import)
                    content = '\n'.join(lines)
                
                # Replace __post_init__ methods
                content = self._replace_post_init_methods(content)
                
                # Write back
                full_path.write_text(content, encoding='utf-8')
                print_success(f"Consolidated config manager: {file_path}")
                
            except Exception as e:
                print_error(f"Error consolidating {file_path}: {e}")
    
    def _replace_post_init_methods(self, content: str) -> str:
        """Replace __post_init__ methods with mixin usage."""
        lines = content.split('\n')
        new_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            
            # Check for class definition
            if line.strip().startswith('class ') and ':' in line:
                # Add mixin to class
                if 'ConfigManagerMixin' not in line:
                    line = line.replace(':', '(ConfigManagerMixin):')
                    new_lines.append(line)
                    continue
            
            # Skip __post_init__ methods
            if 'def __post_init__' in line:
                # Skip the method definition and its content
                skip_next = True
                indent = len(line) - len(line.lstrip())
                j = i + 1
                while j < len(lines) and (lines[j].strip() == '' or 
                                        len(lines[j]) - len(lines[j].lstrip()) > indent):
                    j += 1
                    skip_next = True
                continue
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def run_consolidation(self, dry_run: bool = True) -> Dict:
        """Run the complete consolidation process."""
        print_header("Remaining Duplicate Consolidation")
        
        if dry_run:
            print_info("DRY RUN MODE - No files will be modified")
        
        # Analyze current state
        print_section("Current State")
        print("Files to consolidate:")
        for mixin_name, files in self.files_to_consolidate.items():
            print(f"  {mixin_name}: {len(files)} files")
        
        if dry_run:
            print_info("This would:")
            print("  1. Create mixin utility files")
            print("  2. Consolidate context manager patterns")
            print("  3. Consolidate database cleanup patterns")
            print("  4. Consolidate config manager patterns")
            return {}
        
        # Run consolidation
        print_section("Running Consolidation")
        
        try:
            # Create mixin files
            self.create_mixin_files()
            
            # Consolidate patterns
            self.consolidate_context_managers()
            self.consolidate_database_cleanup()
            self.consolidate_config_managers()
            
            print_success("Consolidation completed successfully!")
            
        except Exception as e:
            print_error(f"Consolidation failed: {e}")
            return {}
        
        return {}

def main():
    """Main consolidation function."""
    consolidator = RemainingDuplicateConsolidator()
    
    # Run dry run first
    print("Running dry run to analyze consolidation opportunities...")
    analysis = consolidator.run_consolidation(dry_run=True)
    
    # Ask for actual consolidation
    response = input("\nProceed with actual consolidation? (y/N): ").strip().lower()
    
    if response != 'y':
        print_info("Consolidation cancelled")
        return
    
    # Run actual consolidation
    print("\nRunning actual consolidation...")
    final_analysis = consolidator.run_consolidation(dry_run=False)
    
    # Print summary
    print_header("Consolidation Summary")
    print("Created mixin utilities:")
    for mixin_name in consolidator.consolidation_patterns.keys():
        print(f"  - {mixin_name}")
    print(f"Backup location: {consolidator.backup_dir}")
    print_success("Remaining duplicate consolidation complete!")

if __name__ == "__main__":
    main() 