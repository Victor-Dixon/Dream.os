"""
Process Management for Browser Operations
Handles Chrome process management and cleanup operations.
"""

import os
import logging
import subprocess
from typing import List

logger = logging.getLogger(__name__)

class ProcessManager:
    """Handles Chrome process management and cleanup."""
    
    @staticmethod
    def kill_existing_chrome_processes():
        """Kill any existing Chrome processes to avoid conflicts."""
        try:
            if os.name == 'nt':  # Windows
                ProcessManager._kill_chrome_windows()
            else:  # Unix-like
                ProcessManager._kill_chrome_unix()
        except Exception as e:
            logger.warning(f"Failed to kill existing Chrome processes: {e}")
    
    @staticmethod
    def _kill_chrome_windows():
        """Kill Chrome processes on Windows."""
        try:
            # Use taskkill to force close Chrome processes
            result = subprocess.run(
                ['taskkill', '/f', '/im', 'chrome.exe'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("Successfully killed existing Chrome processes")
            elif "not found" in result.stderr.lower():
                logger.info("No existing Chrome processes found")
            else:
                logger.warning(f"Taskkill result: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.warning("Timeout while killing Chrome processes")
        except FileNotFoundError:
            logger.warning("taskkill command not found")
        except Exception as e:
            logger.warning(f"Failed to kill Chrome processes on Windows: {e}")
    
    @staticmethod
    def _kill_chrome_unix():
        """Kill Chrome processes on Unix-like systems."""
        try:
            # Use pkill to kill Chrome processes
            result = subprocess.run(
                ['pkill', '-f', 'chrome'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("Successfully killed existing Chrome processes")
            elif result.returncode == 1:
                logger.info("No existing Chrome processes found")
            else:
                logger.warning(f"Pkill result: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.warning("Timeout while killing Chrome processes")
        except FileNotFoundError:
            logger.warning("pkill command not found")
        except Exception as e:
            logger.warning(f"Failed to kill Chrome processes on Unix: {e}")
    
    @staticmethod
    def get_chrome_processes() -> List[str]:
        """
        Get list of running Chrome processes.
        
        Returns:
            List of Chrome process IDs
        """
        try:
            if os.name == 'nt':  # Windows
                return ProcessManager._get_chrome_processes_windows()
            else:  # Unix-like
                return ProcessManager._get_chrome_processes_unix()
        except Exception as e:
            logger.warning(f"Failed to get Chrome processes: {e}")
            return []
    
    @staticmethod
    def _get_chrome_processes_windows() -> List[str]:
        """Get Chrome process IDs on Windows."""
        try:
            result = subprocess.run(
                ['tasklist', '/fi', 'imagename eq chrome.exe', '/fo', 'csv'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                pids = []
                for line in lines:
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            pid = parts[1].strip('"')
                            if pid.isdigit():
                                pids.append(pid)
                return pids
        except Exception as e:
            logger.warning(f"Failed to get Chrome processes on Windows: {e}")
        
        return []
    
    @staticmethod
    def _get_chrome_processes_unix() -> List[str]:
        """Get Chrome process IDs on Unix-like systems."""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'chrome'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                return [pid for pid in pids if pid.strip()]
        except Exception as e:
            logger.warning(f"Failed to get Chrome processes on Unix: {e}")
        
        return [] 