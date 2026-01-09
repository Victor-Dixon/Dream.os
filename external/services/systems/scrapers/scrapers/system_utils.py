"""
System Utilities for Browser Management
Handles disk space checking, temp directory management, and system-level operations.
"""

import os
import tempfile
import logging

logger = logging.getLogger(__name__)

class SystemUtils:
    """Handles system-level utilities for browser operations."""
    
    @staticmethod
    def check_disk_space(path: str = None) -> bool:
        """
        Check if there's sufficient disk space for browser operations.
        
        Args:
            path: Path to check disk space for (defaults to current working directory)
            
        Returns:
            True if sufficient space available, False otherwise
        """
        try:
            if path is None:
                # Check current working directory's drive
                path = os.getcwd()
            
            # Get free space on the drive
            if os.name == 'nt':  # Windows
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes)
                )
                free_gb = free_bytes.value / (1024**3)
            else:  # Unix-like
                statvfs = os.statvfs(path)
                free_gb = (statvfs.f_frsize * statvfs.f_bavail) / (1024**3)
            
            # Require at least 1GB free space
            if free_gb < 1.0:
                logger.warning(f"Low disk space detected: {free_gb:.2f}GB free on {path}")
                return False
            
            logger.info(f"Disk space check passed: {free_gb:.2f}GB free on {path}")
            return True
        except Exception as e:
            logger.warning(f"Could not check disk space: {e}")
            return True  # Assume OK if we can't check
    
    @staticmethod
    def get_temp_dir_with_space() -> str:
        """
        Get a temporary directory with sufficient disk space.
        
        Returns:
            Path to a suitable temporary directory
        """
        # Try common temp directories in order of preference
        temp_dirs = [
            os.environ.get('TEMP'),  # Windows temp
            os.environ.get('TMP'),   # Windows temp alternative
            tempfile.gettempdir(),   # System temp
            os.getcwd(),             # Current directory
            "D:\\temp",              # D: drive temp (if exists)
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir) and SystemUtils.check_disk_space(temp_dir):
                logger.info(f"Using temp directory: {temp_dir}")
                return temp_dir
        
        # Fallback to current directory
        logger.warning("Using current directory as temp directory")
        return os.getcwd()
    
    @staticmethod
    def get_env_bool(env_var: str, default: bool) -> bool:
        """
        Helper method to get boolean from environment variable.
        
        Args:
            env_var: Environment variable name
            default: Default value if environment variable is not set
            
        Returns:
            Boolean value from environment variable or default
        """
        value = os.getenv(env_var)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on') 