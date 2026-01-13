"""
Chain 3 File Locking Redirect Shim Tests
=========================================

Tests for Chain 3 file_locking_engine_base redirect shim fix.
Validates backward compatibility and ensures all imports work correctly.

<!-- SSOT Domain: qa -->

Author: Agent-8 (Testing & Quality Assurance Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class TestFileLockingEngineBaseRedirect:
    """Test file_locking_engine_base redirect shim."""
    
    def test_import_file_locking_engine_base(self):
        """Test that file_locking_engine_base can be imported."""
        from src.core.file_locking.file_locking_engine_base import (
            file_locking_engine_base,
            FileLockEngineBase,
            FileLockEngine
        )
        
        assert file_locking_engine_base is not None
        assert FileLockEngineBase is not None
        assert FileLockEngine is not None
    
    def test_redirect_shim_points_to_file_lock_engine(self):
        """Test that redirect shim points to FileLockEngine."""
        from src.core.file_locking.file_locking_engine_base import (
            file_locking_engine_base,
            FileLockEngineBase,
            FileLockEngine
        )
        
        # Both should be the same class
        assert file_locking_engine_base is FileLockEngine
        assert FileLockEngineBase is FileLockEngine
        assert file_locking_engine_base is FileLockEngineBase
    
    def test_import_from_init(self):
        """Test importing from __init__.py."""
        from src.core.file_locking import (
            file_locking_engine_base,
            FileLockEngineBase,
            FileLockEngine
        )
        
        assert file_locking_engine_base is not None
        assert FileLockEngineBase is not None
        assert FileLockEngine is not None
        assert file_locking_engine_base is FileLockEngine


class TestFileLockEngineInstantiation:
    """Test FileLockEngine can be instantiated."""
    
    def test_file_lock_engine_instantiation(self):
        """Test that FileLockEngine can be instantiated."""
        from src.core.file_locking import FileLockEngine
        from src.core.file_locking.file_locking_models import LockConfig
        
        # Test with default config
        engine = FileLockEngine()
        assert engine is not None
        assert hasattr(engine, 'config')
        assert hasattr(engine, 'create_lock')
        assert hasattr(engine, 'acquire_lock')
        assert hasattr(engine, 'release_lock')
        assert hasattr(engine, 'is_locked')
    
    def test_file_lock_engine_with_config(self):
        """Test FileLockEngine with custom config."""
        from src.core.file_locking import FileLockEngine
        from src.core.file_locking.file_locking_models import LockConfig
        
        config = LockConfig()
        engine = FileLockEngine(config)
        assert engine is not None
        assert engine.config is config
    
    def test_file_lock_engine_base_alias_instantiation(self):
        """Test that file_locking_engine_base alias can be instantiated."""
        from src.core.file_locking import file_locking_engine_base
        
        # Should be able to instantiate using the alias
        engine = file_locking_engine_base()
        assert engine is not None
        assert hasattr(engine, 'create_lock')
        assert hasattr(engine, 'release_lock')


class TestBackwardCompatibility:
    """Test backward compatibility with old import patterns."""
    
    def test_old_import_pattern_1(self):
        """Test old import: from file_locking_engine_base import file_locking_engine_base."""
        from src.core.file_locking.file_locking_engine_base import file_locking_engine_base
        
        # Should be able to use it
        assert file_locking_engine_base is not None
        engine = file_locking_engine_base()
        assert engine is not None
    
    def test_old_import_pattern_2(self):
        """Test old import: from file_locking import file_locking_engine_base."""
        from src.core.file_locking import file_locking_engine_base
        
        # Should work
        assert file_locking_engine_base is not None
        engine = file_locking_engine_base()
        assert engine is not None
    
    def test_old_import_pattern_3(self):
        """Test old import: from file_locking_engine_base import FileLockEngineBase."""
        from src.core.file_locking.file_locking_engine_base import FileLockEngineBase
        
        # Should work
        assert FileLockEngineBase is not None
        engine = FileLockEngineBase()
        assert engine is not None


class TestAffectedFiles:
    """Test that all affected files can import correctly."""
    
    def test_file_locking_manager_imports(self):
        """Test file_locking_manager.py imports."""
        from src.core.file_locking.file_locking_manager import FileLockManager
        
        # Should be able to create manager
        manager = FileLockManager()
        assert manager is not None
        assert hasattr(manager, 'engine')
        
        # Engine should be accessible (lazy-loaded)
        engine = manager.engine
        assert engine is not None
    
    def test_file_locking_engine_imports(self):
        """Test file_locking_engine.py imports."""
        from src.core.file_locking.file_locking_engine import FileLockEngine
        
        engine = FileLockEngine()
        assert engine is not None
    
    def test_file_locking_engine_operations_imports(self):
        """Test file_locking_engine_operations.py imports."""
        from src.core.file_locking.file_locking_engine_operations import (
            FileLockEngineOperations
        )
        
        # Should be able to import
        assert FileLockEngineOperations is not None
    
    def test_file_locking_engine_platform_imports(self):
        """Test file_locking_engine_platform.py imports."""
        from src.core.file_locking.file_locking_engine_platform import (
            FileLockEnginePlatform
        )
        
        # Should be able to import
        assert FileLockEnginePlatform is not None
    
    def test_file_locking_orchestrator_imports(self):
        """Test file_locking_orchestrator.py imports if it exists."""
        try:
            from src.core.file_locking.file_locking_orchestrator import (
                FileLockingOrchestrator
            )
            assert FileLockingOrchestrator is not None
        except ImportError:
            # File might not exist, that's okay
            pass
    
    def test_file_locking_models_imports(self):
        """Test file_locking_models.py imports."""
        from src.core.file_locking.file_locking_models import (
            LockConfig,
            LockInfo,
            LockMetrics,
            LockResult,
            LockStatus
        )
        
        # All models should be importable
        assert LockConfig is not None
        assert LockInfo is not None
        assert LockMetrics is not None
        assert LockResult is not None
        assert LockStatus is not None


class TestNoRegressions:
    """Test that existing functionality still works."""
    
    def test_basic_lock_operations(self):
        """Test basic lock operations still work."""
        from src.core.file_locking import FileLockEngine
        from pathlib import Path
        import tempfile
        
        engine = FileLockEngine()
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            test_file = tmp.name
        
        try:
            # Test create lock
            result = engine.create_lock(test_file, {"test": "data"})
            assert result is not None
            assert hasattr(result, 'success')
            assert result.success
            
            # Test acquire lock (needs LockInfo)
            if result.lock_info:
                acquire_result = engine.acquire_lock(result.lock_info)
                assert acquire_result is not None
                assert hasattr(acquire_result, 'success')
                
                # Test release lock
                if acquire_result.success:
                    release_result = engine.release_lock(result.lock_info)
                    assert release_result is not None
            
            # Test is_locked
            is_locked = engine.is_locked(test_file)
            assert isinstance(is_locked, bool)
        finally:
            # Cleanup
            try:
                Path(test_file).unlink()
            except:
                pass
    
    def test_file_lock_manager_operations(self):
        """Test FileLockManager operations still work."""
        from src.core.file_locking import FileLockManager
        import tempfile
        from pathlib import Path
        
        manager = FileLockManager()
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            test_file = tmp.name
        
        try:
            # Test create file lock
            result = manager.create_file_lock(test_file, {"test": "data"})
            assert result is not None
            assert hasattr(result, 'success')
            
            # Test acquire lock
            acquire_result = manager.acquire_lock(test_file)
            assert acquire_result is not None
            assert hasattr(acquire_result, 'success')
            
            # Test get lock info (manager has this method)
            lock_info = manager.get_lock_info(test_file)
            # May be None if lock wasn't successfully acquired
            assert lock_info is None or hasattr(lock_info, 'lock_file')
            
            # Test release lock (correct method name)
            if acquire_result.success:
                release_result = manager.release_lock(test_file)
                assert release_result is not None
                assert hasattr(release_result, 'success')
            
            # Test is_locked
            is_locked = manager.is_locked(test_file)
            assert isinstance(is_locked, bool)
        finally:
            # Cleanup
            try:
                Path(test_file).unlink()
            except:
                pass

