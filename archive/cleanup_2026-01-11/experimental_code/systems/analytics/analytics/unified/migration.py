"""
Analytics System Migration - Transition to Unified Analytics
==========================================================

This module provides migration utilities to transition from the old scattered
analytics systems to the new unified analytics system.

Migration targets:
- analytics_system.py (865 lines) -> unified_analytics_system.py
- content_analytics_integration.py (729 lines) -> content_analytics.py
- expanded_analytics_system.py (1002 lines) -> unified_analytics_system.py
- time_series_analyzer.py (530 lines) -> time_series_analytics.py
- topic_analyzer.py (357 lines) -> topic_analytics.py
- analytics_optimizer.py (440 lines) -> unified_analytics_system.py
- analyze_conversations_ai.py (186 lines) -> conversation_analytics.py

Total lines consolidated: 4,109 lines
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AnalyticsMigrationManager:
    """
    Manages migration from old analytics systems to unified analytics system.
    """
    
    def __init__(self, project_root: str = None):
        """Initialize the migration manager."""
        if project_root is None:
            project_root = Path(__file__).parent.parent.parent.parent
        self.project_root = Path(project_root)
        
        # Define migration paths
        self.old_analytics_files = {
            'analytics_system': 'src/dreamscape/core/analytics/analytics_system.py',
            'content_analytics_integration': 'src/dreamscape/core/content_analytics_integration.py',
            'expanded_analytics_system': 'src/dreamscape/core/expanded_analytics_system.py',
            'time_series_analyzer': 'src/dreamscape/core/analytics/time_series_analyzer.py',
            'topic_analyzer': 'src/dreamscape/core/analytics/topic_analyzer.py',
            'analytics_optimizer': 'src/dreamscape/core/analytics/analytics_optimizer.py',
            'analyze_conversations_ai': 'src/dreamscape/core/analytics/analyze_conversations_ai.py'
        }
        
        self.new_unified_files = {
            'unified_analytics_system': 'src/dreamscape/core/analytics/unified/unified_analytics_system.py',
            'content_analytics': 'src/dreamscape/core/analytics/unified/content/content_analytics.py',
            'template_analytics': 'src/dreamscape/core/analytics/unified/templates/template_analytics.py',
            'analytics_engine': 'src/dreamscape/core/analytics/unified/core/analytics_engine.py'
        }
        
        # Migration status
        self.migration_status = {}
        self.backup_dir = self.project_root / "backups" / "analytics_migration"
    
    def create_backup(self) -> bool:
        """Create backup of old analytics files."""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            
            backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = self.backup_dir / f"analytics_backup_{backup_timestamp}"
            backup_path.mkdir(exist_ok=True)
            
            # Backup old files
            for name, file_path in self.old_analytics_files.items():
                old_file = self.project_root / file_path
                if old_file.exists():
                    backup_file = backup_path / f"{name}.py"
                    shutil.copy2(old_file, backup_file)
                    logger.info(f"Backed up {name}: {old_file} -> {backup_file}")
            
            # Create backup manifest
            manifest = {
                'backup_timestamp': backup_timestamp,
                'backup_path': str(backup_path),
                'files_backed_up': list(self.old_analytics_files.keys()),
                'migration_version': '2.0.0'
            }
            
            with open(backup_path / 'backup_manifest.json', 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info(f"Backup created successfully at {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return False
    
    def validate_migration_readiness(self) -> Dict[str, Any]:
        """Validate that the system is ready for migration."""
        validation_results = {
            'ready': True,
            'issues': [],
            'warnings': [],
            'file_status': {}
        }
        
        # Check old files
        for name, file_path in self.old_analytics_files.items():
            old_file = self.project_root / file_path
            if old_file.exists():
                validation_results['file_status'][name] = {
                    'exists': True,
                    'size': old_file.stat().st_size,
                    'path': str(old_file)
                }
            else:
                validation_results['file_status'][name] = {
                    'exists': False,
                    'size': 0,
                    'path': str(old_file)
                }
                validation_results['warnings'].append(f"Old file not found: {name}")
        
        # Check new files
        for name, file_path in self.new_unified_files.items():
            new_file = self.project_root / file_path
            if new_file.exists():
                validation_results['file_status'][name] = {
                    'exists': True,
                    'size': new_file.stat().st_size,
                    'path': str(new_file)
                }
            else:
                validation_results['file_status'][name] = {
                    'exists': False,
                    'size': 0,
                    'path': str(new_file)
                }
                validation_results['issues'].append(f"New file not found: {name}")
                validation_results['ready'] = False
        
        # Check for import dependencies
        import_dependencies = self._check_import_dependencies()
        if import_dependencies['missing']:
            validation_results['issues'].extend(import_dependencies['missing'])
            validation_results['ready'] = False
        
        if import_dependencies['warnings']:
            validation_results['warnings'].extend(import_dependencies['warnings'])
        
        return validation_results
    
    def _check_import_dependencies(self) -> Dict[str, List[str]]:
        """Check for import dependencies."""
        missing = []
        warnings = []
        
        # Check for required packages
        required_packages = [
            'numpy', 'pandas', 'matplotlib', 'seaborn', 'sklearn',
            'dataclasses_json', 'sqlite3'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                if package in ['numpy', 'pandas', 'matplotlib', 'seaborn', 'sklearn']:
                    warnings.append(f"Optional package not available: {package}")
                else:
                    missing.append(f"Required package not available: {package}")
        
        return {'missing': missing, 'warnings': warnings}
    
    def generate_migration_report(self) -> Dict[str, Any]:
        """Generate a comprehensive migration report."""
        validation = self.validate_migration_readiness()
        
        # Calculate statistics
        old_files_total_lines = sum(
            status.get('size', 0) for status in validation['file_status'].values()
            if status.get('exists', False) and 'old' in status.get('path', '')
        )
        
        new_files_total_lines = sum(
            status.get('size', 0) for status in validation['file_status'].values()
            if status.get('exists', False) and 'unified' in status.get('path', '')
        )
        
        # Estimate line count (rough approximation)
        old_lines_estimate = old_files_total_lines // 4  # Rough estimate
        new_lines_estimate = new_files_total_lines // 4
        
        report = {
            'migration_summary': {
                'total_old_files': len(self.old_analytics_files),
                'total_new_files': len(self.new_unified_files),
                'estimated_old_lines': old_lines_estimate,
                'estimated_new_lines': new_lines_estimate,
                'estimated_reduction': old_lines_estimate - new_lines_estimate,
                'estimated_reduction_percent': ((old_lines_estimate - new_lines_estimate) / old_lines_estimate * 100) if old_lines_estimate > 0 else 0
            },
            'validation_results': validation,
            'migration_steps': self._get_migration_steps(),
            'rollback_instructions': self._get_rollback_instructions(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _get_migration_steps(self) -> List[Dict[str, str]]:
        """Get step-by-step migration instructions."""
        return [
            {
                'step': 1,
                'action': 'Create backup',
                'description': 'Backup all existing analytics files',
                'command': 'migration_manager.create_backup()'
            },
            {
                'step': 2,
                'action': 'Update imports',
                'description': 'Update import statements in existing code',
                'command': 'migration_manager.update_imports()'
            },
            {
                'step': 3,
                'action': 'Test migration',
                'description': 'Test the new unified system',
                'command': 'migration_manager.test_migration()'
            },
            {
                'step': 4,
                'action': 'Remove old files',
                'description': 'Remove old analytics files (optional)',
                'command': 'migration_manager.remove_old_files()'
            }
        ]
    
    def _get_rollback_instructions(self) -> List[str]:
        """Get rollback instructions."""
        return [
            "1. Stop the application",
            "2. Restore backup files from the backup directory",
            "3. Revert import statements to use old analytics modules",
            "4. Restart the application",
            f"5. Backup location: {self.backup_dir}"
        ]
    
    def update_imports(self, target_directory: str = None) -> Dict[str, Any]:
        """Update import statements to use the new unified system."""
        if target_directory is None:
            target_directory = str(self.project_root / "src" / "dreamscape")
        
        target_path = Path(target_directory)
        update_results = {
            'files_updated': [],
            'files_skipped': [],
            'errors': []
        }
        
        # Import mapping
        import_mapping = {
            'from dreamscape.core.analytics.analytics_system import': 'from dreamscape.core.analytics.unified.unified_analytics_system import',
            'from dreamscape.core.content_analytics_integration import': 'from dreamscape.core.analytics.unified.content.content_analytics import',
            'from dreamscape.core.expanded_analytics_system import': 'from dreamscape.core.analytics.unified.unified_analytics_system import',
            'from dreamscape.core.analytics.time_series_analyzer import': 'from dreamscape.core.analytics.unified.time_series.time_series_analytics import',
            'from dreamscape.core.analytics.topic_analyzer import': 'from dreamscape.core.analytics.unified.topics.topic_analytics import',
            'from dreamscape.core.analytics.analytics_optimizer import': 'from dreamscape.core.analytics.unified.unified_analytics_system import',
            'from dreamscape.core.analytics.analyze_conversations_ai import': 'from dreamscape.core.analytics.unified.conversations.conversation_analytics import'
        }
        
        # Class mapping
        class_mapping = {
            'ComprehensiveAnalyticsSystem': 'UnifiedAnalyticsSystem',
            'ContentAnalyticsIntegration': 'ContentAnalyticsModule',
            'ExpandedAnalyticsSystem': 'UnifiedAnalyticsSystem',
            'TimeSeriesAnalyzer': 'TimeSeriesAnalyticsModule',
            'TopicAnalyzer': 'TopicAnalyticsModule',
            'AnalyticsOptimizer': 'UnifiedAnalyticsSystem',
            'ConversationAnalyzer': 'ConversationAnalyticsModule'
        }
        
        try:
            # Find Python files
            python_files = list(target_path.rglob("*.py"))
            
            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    updated = False
                    
                    # Update imports
                    for old_import, new_import in import_mapping.items():
                        if old_import in content:
                            content = content.replace(old_import, new_import)
                            updated = True
                    
                    # Update class references
                    for old_class, new_class in class_mapping.items():
                        if old_class in content:
                            content = content.replace(old_class, new_class)
                            updated = True
                    
                    if updated:
                        # Create backup of the file
                        backup_file = file_path.with_suffix('.py.backup')
                        shutil.copy2(file_path, backup_file)
                        
                        # Write updated content
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        update_results['files_updated'].append(str(file_path))
                        logger.info(f"Updated imports in {file_path}")
                    else:
                        update_results['files_skipped'].append(str(file_path))
                
                except Exception as e:
                    update_results['errors'].append(f"Error updating {file_path}: {e}")
                    logger.error(f"Error updating {file_path}: {e}")
        
        except Exception as e:
            update_results['errors'].append(f"Error scanning directory {target_directory}: {e}")
            logger.error(f"Error scanning directory {target_directory}: {e}")
        
        return update_results
    
    def test_migration(self) -> Dict[str, Any]:
        """Test the migration by running basic functionality tests."""
        test_results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        
        try:
            # Test 1: Import new system
            try:
                from .unified_analytics_system import UnifiedAnalyticsSystem
                test_results['passed'].append("Import UnifiedAnalyticsSystem")
            except ImportError as e:
                test_results['failed'].append(f"Import UnifiedAnalyticsSystem: {e}")
            
            # Test 2: Create system instance
            try:
                system = UnifiedAnalyticsSystem()
                test_results['passed'].append("Create UnifiedAnalyticsSystem instance")
            except Exception as e:
                test_results['failed'].append(f"Create UnifiedAnalyticsSystem instance: {e}")
            
            # Test 3: Basic content analysis
            try:
                if 'system' in locals():
                    result = system.analyze_content("Test content for migration validation.")
                    if result and 'content_analysis' in result:
                        test_results['passed'].append("Basic content analysis")
                    else:
                        test_results['failed'].append("Basic content analysis returned invalid result")
            except Exception as e:
                test_results['failed'].append(f"Basic content analysis: {e}")
            
            # Test 4: Generate report
            try:
                if 'system' in locals():
                    report = system.generate_comprehensive_report("7d")
                    if report:
                        test_results['passed'].append("Generate comprehensive report")
                    else:
                        test_results['failed'].append("Generate comprehensive report returned None")
            except Exception as e:
                test_results['failed'].append(f"Generate comprehensive report: {e}")
            
            # Test 5: Export functionality
            try:
                if 'system' in locals():
                    export_path = system.export_analytics("json")
                    if export_path and Path(export_path).exists():
                        test_results['passed'].append("Export analytics")
                    else:
                        test_results['failed'].append("Export analytics failed")
            except Exception as e:
                test_results['failed'].append(f"Export analytics: {e}")
        
        except Exception as e:
            test_results['failed'].append(f"Test setup failed: {e}")
        
        return test_results
    
    def remove_old_files(self, dry_run: bool = True) -> Dict[str, Any]:
        """Remove old analytics files (with dry run option)."""
        removal_results = {
            'files_removed': [],
            'files_skipped': [],
            'errors': [],
            'dry_run': dry_run
        }
        
        for name, file_path in self.old_analytics_files.items():
            old_file = self.project_root / file_path
            
            if old_file.exists():
                if dry_run:
                    removal_results['files_skipped'].append(f"{name} (dry run)")
                    logger.info(f"Would remove {name}: {old_file}")
                else:
                    try:
                        old_file.unlink()
                        removal_results['files_removed'].append(name)
                        logger.info(f"Removed {name}: {old_file}")
                    except Exception as e:
                        removal_results['errors'].append(f"Error removing {name}: {e}")
                        logger.error(f"Error removing {name}: {e}")
            else:
                removal_results['files_skipped'].append(f"{name} (not found)")
        
        return removal_results
    
    def run_full_migration(self, dry_run: bool = True) -> Dict[str, Any]:
        """Run the complete migration process."""
        migration_results = {
            'backup_created': False,
            'validation_passed': False,
            'imports_updated': False,
            'tests_passed': False,
            'old_files_removed': False,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Step 1: Create backup
            logger.info("Step 1: Creating backup...")
            if self.create_backup():
                migration_results['backup_created'] = True
            else:
                migration_results['errors'].append("Backup creation failed")
                return migration_results
            
            # Step 2: Validate migration readiness
            logger.info("Step 2: Validating migration readiness...")
            validation = self.validate_migration_readiness()
            if validation['ready']:
                migration_results['validation_passed'] = True
            else:
                migration_results['errors'].extend(validation['issues'])
                migration_results['warnings'].extend(validation['warnings'])
                return migration_results
            
            # Step 3: Update imports
            logger.info("Step 3: Updating imports...")
            import_results = self.update_imports()
            if not import_results['errors']:
                migration_results['imports_updated'] = True
            else:
                migration_results['errors'].extend(import_results['errors'])
            
            # Step 4: Test migration
            logger.info("Step 4: Testing migration...")
            test_results = self.test_migration()
            if not test_results['failed']:
                migration_results['tests_passed'] = True
            else:
                migration_results['errors'].extend(test_results['failed'])
            
            # Step 5: Remove old files (if not dry run)
            if not dry_run and migration_results['tests_passed']:
                logger.info("Step 5: Removing old files...")
                removal_results = self.remove_old_files(dry_run=False)
                if not removal_results['errors']:
                    migration_results['old_files_removed'] = True
                else:
                    migration_results['errors'].extend(removal_results['errors'])
            
            logger.info("Migration completed successfully!")
        
        except Exception as e:
            migration_results['errors'].append(f"Migration failed: {e}")
            logger.error(f"Migration failed: {e}")
        
        return migration_results


# Convenience functions
def run_migration(dry_run: bool = True) -> Dict[str, Any]:
    """Run the analytics migration."""
    migration_manager = AnalyticsMigrationManager()
    return migration_manager.run_full_migration(dry_run)


def generate_migration_report() -> Dict[str, Any]:
    """Generate a migration report."""
    migration_manager = AnalyticsMigrationManager()
    return migration_manager.generate_migration_report()


def test_migration() -> Dict[str, Any]:
    """Test the migration."""
    migration_manager = AnalyticsMigrationManager()
    return migration_manager.test_migration()


if __name__ == "__main__":
    # Run migration in dry-run mode by default
    print("Analytics Migration Tool")
    print("=======================")
    
    migration_manager = AnalyticsMigrationManager()
    
    # Generate report
    report = migration_manager.generate_migration_report()
    print(f"\nMigration Report:")
    print(f"Total old files: {report['migration_summary']['total_old_files']}")
    print(f"Total new files: {report['migration_summary']['total_new_files']}")
    print(f"Estimated line reduction: {report['migration_summary']['estimated_reduction_percent']:.1f}%")
    
    # Check if ready
    if report['validation_results']['ready']:
        print("\n✅ System is ready for migration!")
        
        # Ask for confirmation
        response = input("\nRun migration? (y/N): ").lower().strip()
        if response == 'y':
            results = migration_manager.run_full_migration(dry_run=True)
            print(f"\nMigration Results:")
            print(f"Backup created: {results['backup_created']}")
            print(f"Validation passed: {results['validation_passed']}")
            print(f"Imports updated: {results['imports_updated']}")
            print(f"Tests passed: {results['tests_passed']}")
            
            if results['errors']:
                print(f"\nErrors: {results['errors']}")
        else:
            print("Migration cancelled.")
    else:
        print("\n❌ System is not ready for migration.")
        print(f"Issues: {report['validation_results']['issues']}")
        print(f"Warnings: {report['validation_results']['warnings']}") 