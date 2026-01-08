"""
Cleanup Command Handler - V2 Compliant (<400 lines)
Handles system cleanup and maintenance operations.
"""

import os
import shutil
from typing import List, Set, Dict, Any, Tuple
from pathlib import Path
from src.services.service_manager import ServiceManager


class CleanupHandler:
    """Handles cleanup command with safe file and cache management."""

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager
        self.safe_cleanup_patterns = {
            '__pycache__',
            '*.pyc',
            '*.pyo',
            '.pytest_cache',
            'node_modules/.cache',
            '*.log',
            'logs/*.log',
            'temp/*',
            'tmp/*'
        }

    def execute(self) -> None:
        """Execute cleanup command."""
        print("🧹 dream.os - System Cleanup")
        print("=" * 35)

        print("This will clean up temporary files and caches.")
        print("Safe cleanup targets:")
        for pattern in sorted(self.safe_cleanup_patterns):
            print(f"   • {pattern}")

        try:
            confirm = input("\nContinue? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ Cleanup cancelled.")
                return
        except KeyboardInterrupt:
            print("\n❌ Cleanup cancelled.")
            return

        print("\n🧹 Starting cleanup...")

        # Stop services first for safe cleanup
        print("   Stopping services for safe cleanup...")
        try:
            self.service_manager.stop_all_services()
            print("   ✅ Services stopped")
        except Exception as e:
            print(f"   ⚠️  Warning: Could not stop all services: {e}")
            print("   Continuing with cleanup anyway...")

        # Perform cleanup
        cleanup_results = self._perform_cleanup()

        # Display results
        self._display_cleanup_results(cleanup_results)

        # Restart services
        print("\n🔄 Restarting services...")
        try:
            self.service_manager.start_all_services()
            print("   ✅ Services restarted")
        except Exception as e:
            print(f"   ⚠️  Warning: Could not restart services: {e}")
            print("   💡 Manual restart: python main.py --start")

        print("\n✅ Cleanup completed!")

    def _perform_cleanup(self) -> Dict[str, Any]:
        """Perform the actual cleanup operations."""
        results = {
            'files_removed': 0,
            'dirs_removed': 0,
            'bytes_freed': 0,
            'errors': []
        }

        # Clean cache directories
        cache_dirs = ['__pycache__', '.pytest_cache', 'node_modules/.cache']
        for cache_dir in cache_dirs:
            try:
                removed = self._clean_directory(cache_dir)
                results['dirs_removed'] += removed
            except Exception as e:
                results['errors'].append(f"Cache cleanup error: {e}")

        # Clean temp files
        temp_patterns = ['*.pyc', '*.pyo', '*.log', 'logs/*.log']
        for pattern in temp_patterns:
            try:
                removed, bytes_freed = self._clean_files_by_pattern(pattern)
                results['files_removed'] += removed
                results['bytes_freed'] += bytes_freed
            except Exception as e:
                results['errors'].append(f"File cleanup error: {e}")

        # Clean temp directories
        temp_dirs = ['temp', 'tmp']
        for temp_dir in temp_dirs:
            try:
                removed, bytes_freed = self._clean_temp_directory(temp_dir)
                results['files_removed'] += removed
                results['bytes_freed'] += bytes_freed
            except Exception as e:
                results['errors'].append(f"Temp cleanup error: {e}")

        return results

    def _clean_directory(self, dirname: str) -> int:
        """Clean all instances of a directory name recursively."""
        removed_count = 0
        for root, dirs, files in os.walk('.'):
            if dirname in dirs:
                full_path = os.path.join(root, dirname)
                try:
                    shutil.rmtree(full_path)
                    removed_count += 1
                except Exception:
                    pass  # Skip if can't remove
        return removed_count

    def _clean_files_by_pattern(self, pattern: str) -> Tuple[int, int]:
        """Clean files matching a pattern. Returns (files_removed, bytes_freed)."""
        removed_count = 0
        bytes_freed = 0

        if '*' in pattern:
            # Handle glob patterns
            import glob
            for filepath in glob.glob(pattern, recursive=True):
                try:
                    size = os.path.getsize(filepath)
                    os.remove(filepath)
                    removed_count += 1
                    bytes_freed += size
                except Exception:
                    pass  # Skip if can't remove
        else:
            # Handle directory patterns
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith(pattern.replace('*', '')):
                        filepath = os.path.join(root, file)
                        try:
                            size = os.path.getsize(filepath)
                            os.remove(filepath)
                            removed_count += 1
                            bytes_freed += size
                        except Exception:
                            pass  # Skip if can't remove

        return removed_count, bytes_freed

    def _clean_temp_directory(self, dirname: str) -> Tuple[int, int]:
        """Clean contents of a temporary directory."""
        removed_count = 0
        bytes_freed = 0

        if os.path.exists(dirname):
            for root, dirs, files in os.walk(dirname):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        os.remove(filepath)
                        removed_count += 1
                        bytes_freed += size
                    except Exception:
                        pass  # Skip if can't remove

        return removed_count, bytes_freed

    def _display_cleanup_results(self, results: Dict[str, Any]) -> None:
        """Display cleanup results."""
        print("\n📊 CLEANUP RESULTS:")
        print(f"   Files removed: {results['files_removed']}")
        print(f"   Directories removed: {results['dirs_removed']}")
        print(f"   Bytes freed: {results['bytes_freed']:.1f}")
        if results['errors']:
            print(f"\n⚠️  ERRORS ({len(results['errors'])}):")
            for error in results['errors'][:3]:  # Show first 3 errors
                print(f"   • {error}")
            if len(results['errors']) > 3:
                print(f"   • ... and {len(results['errors']) - 3} more")

        if results['bytes_freed'] > 0:
            print("\n💾 Disk space recovered!")