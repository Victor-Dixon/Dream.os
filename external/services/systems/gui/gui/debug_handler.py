#!/usr/bin/env python3
"""
GUI Debug Handler
================

Comprehensive debugging and error handling system for all GUI interactions.
Provides detailed logging, error tracking, and user feedback for maintainability.
"""

import logging
import traceback
import sys
import time
from datetime import datetime
from typing import Callable, Any, Dict, Optional, Union
from functools import wraps
from pathlib import Path

from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import QObject, pyqtSignal, QThread

logger = logging.getLogger(__name__)

class GUIDebugHandler(QObject):
    """Centralized GUI debugging and error handling system."""
    
    # Signals for cross-thread communication
    error_occurred = pyqtSignal(str, str, str)  # button_name, error_message, stack_trace
    button_clicked = pyqtSignal(str, str)  # button_name, panel_name
    operation_started = pyqtSignal(str, str)  # operation_name, panel_name
    operation_completed = pyqtSignal(str, str, bool)  # operation_name, panel_name, success
    
    def __init__(self):
        super().__init__()
        self.debug_log_file = Path("logs/gui_debug.log")
        self.debug_log_file.parent.mkdir(exist_ok=True)
        
        # Setup debug logging
        self._setup_debug_logging()
        
        # Statistics tracking
        self.button_click_count = {}
        self.error_count = {}
        self.operation_times = {}
        
        # Connect signals to handlers
        self.error_occurred.connect(self._log_error)
        self.button_clicked.connect(self._log_button_click)
        self.operation_started.connect(self._log_operation_start)
        self.operation_completed.connect(self._log_operation_complete)
    
    def _setup_debug_logging(self):
        """Setup dedicated debug logging."""
        debug_handler = logging.FileHandler(self.debug_log_file)
        debug_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        debug_handler.setFormatter(formatter)
        
        # Create debug logger
        debug_logger = logging.getLogger('gui_debug')
        debug_logger.setLevel(logging.DEBUG)
        debug_logger.addHandler(debug_handler)
        debug_logger.propagate = False
        
        self.debug_logger = debug_logger
    
    def debug_button_click(self, button_name: str, panel_name: str = "Unknown"):
        """Decorator for debugging button clicks."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                operation_id = f"{panel_name}.{button_name}"
                
                try:
                    # Log button click
                    self.debug_logger.info(f"Button clicked: {button_name} in {panel_name}")
                    self.button_clicked.emit(button_name, panel_name)
                    
                    # Track operation start
                    self.operation_started.emit(operation_id, panel_name)
                    
                    # Execute the function
                    result = func(*args, **kwargs)
                    
                    # Track successful completion
                    execution_time = time.time() - start_time
                    self.operation_completed.emit(operation_id, panel_name, True)
                    
                    self.debug_logger.info(
                        f"Button operation completed: {button_name} in {panel_name} "
                        f"(took {execution_time:.3f}s)"
                    )
                    
                    return result
                    
                except Exception as e:
                    # Track error
                    execution_time = time.time() - start_time
                    error_msg = str(e)
                    stack_trace = traceback.format_exc()
                    
                    self.error_occurred.emit(button_name, error_msg, stack_trace)
                    self.operation_completed.emit(operation_id, panel_name, False)
                    
                    self.debug_logger.error(
                        f"Button operation failed: {button_name} in {panel_name} "
                        f"(took {execution_time:.3f}s) - {error_msg}"
                    )
                    self.debug_logger.debug(f"Stack trace: {stack_trace}")
                    
                    # Show user-friendly error message
                    self._show_error_dialog(button_name, panel_name, error_msg)
                    
                    # Re-raise the exception for proper error handling
                    raise
                    
            return wrapper
        return decorator
    
    def debug_operation(self, operation_name: str, panel_name: str = "Unknown"):
        """Decorator for debugging general operations."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                operation_id = f"{panel_name}.{operation_name}"
                
                try:
                    # Log operation start
                    self.debug_logger.info(f"🚀 Operation started: {operation_name} in {panel_name}")
                    self.operation_started.emit(operation_id, panel_name)
                    
                    # Execute the function
                    result = func(*args, **kwargs)
                    
                    # Track successful completion
                    execution_time = time.time() - start_time
                    self.operation_completed.emit(operation_id, panel_name, True)
                    
                    self.debug_logger.info(
                        f"PASS Operation completed: {operation_name} in {panel_name} "
                        f"(took {execution_time:.3f}s)"
                    )
                    
                    return result
                    
                except Exception as e:
                    # Track error
                    execution_time = time.time() - start_time
                    error_msg = str(e)
                    stack_trace = traceback.format_exc()
                    
                    self.error_occurred.emit(operation_name, error_msg, stack_trace)
                    self.operation_completed.emit(operation_id, panel_name, False)
                    
                    self.debug_logger.error(
                        f"FAIL Operation failed: {operation_name} in {panel_name} "
                        f"(took {execution_time:.3f}s) - {error_msg}"
                    )
                    self.debug_logger.debug(f"Stack trace: {stack_trace}")
                    
                    # Show user-friendly error message
                    self._show_error_dialog(operation_name, panel_name, error_msg)
                    
                    # Re-raise the exception for proper error handling
                    raise
                    
            return wrapper
        return decorator
    
    def _log_error(self, button_name: str, error_message: str, stack_trace: str):
        """Log error details."""
        if button_name not in self.error_count:
            self.error_count[button_name] = 0
        self.error_count[button_name] += 1
        
        self.debug_logger.error(f"Error in {button_name}: {error_message}")
        self.debug_logger.debug(f"Stack trace: {stack_trace}")
    
    def _log_button_click(self, button_name: str, panel_name: str):
        """Log button click."""
        if button_name not in self.button_click_count:
            self.button_click_count[button_name] = 0
        self.button_click_count[button_name] += 1
        
        self.debug_logger.info(f"Button clicked: {button_name} in {panel_name}")
    
    def _log_operation_start(self, operation_name: str, panel_name: str):
        """Log operation start."""
        self.operation_times[operation_name] = time.time()
        self.debug_logger.info(f"Operation started: {operation_name} in {panel_name}")
    
    def _log_operation_complete(self, operation_name: str, panel_name: str, success: bool):
        """Log operation completion."""
        if operation_name in self.operation_times:
            execution_time = time.time() - self.operation_times[operation_name]
            status = "PASS" if success else "FAIL"
            self.debug_logger.info(
                f"{status} Operation completed: {operation_name} in {panel_name} "
                f"(took {execution_time:.3f}s)"
            )
    
    def _show_error_dialog(self, button_name: str, panel_name: str, error_message: str):
        """Show user-friendly error dialog."""
        try:
            # Get the main application window
            app = QApplication.instance()
            if app and app.activeWindow():
                parent = app.activeWindow()
            else:
                parent = None
            
            # Create detailed error message
            detailed_message = (
                f"Button: {button_name}\n"
                f"Panel: {panel_name}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Error: {error_message}\n\n"
                f"Debug information has been logged to:\n{self.debug_log_file}"
            )
            
            # Show error dialog
            QMessageBox.critical(
                parent,
                f"GUI Error - {button_name}",
                f"An error occurred while processing the '{button_name}' button:\n\n{error_message}\n\n"
                f"Please check the debug log for more details.",
                QMessageBox.StandardButton.Ok
            )
            
        except Exception as e:
            # Fallback error logging if dialog fails
            logger.error(f"Failed to show error dialog: {e}")
            logger.error(f"Original error: {button_name} in {panel_name} - {error_message}")
    
    def get_debug_statistics(self) -> Dict[str, Any]:
        """Get debug statistics."""
        return {
            "button_clicks": dict(self.button_click_count),
            "errors": dict(self.error_count),
            "total_operations": len(self.operation_times),
            "debug_log_file": str(self.debug_log_file),
            "timestamp": datetime.now().isoformat()
        }
    
    def clear_statistics(self):
        """Clear debug statistics."""
        self.button_click_count.clear()
        self.error_count.clear()
        self.operation_times.clear()
        self.debug_logger.info("Debug statistics cleared")
    
    def export_debug_report(self, output_file: str = None) -> str:
        """Export comprehensive debug report."""
        if output_file is None:
            output_file = f"debug_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report_path = Path(output_file)
        
        with open(report_path, 'w') as f:
            f.write("=== DREAMSCAPE GUI DEBUG REPORT ===\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write("=== BUTTON CLICK STATISTICS ===\n")
            for button, count in self.button_click_count.items():
                f.write(f"{button}: {count} clicks\n")
            
            f.write("\n=== ERROR STATISTICS ===\n")
            for button, count in self.error_count.items():
                f.write(f"{button}: {count} errors\n")
            
            f.write(f"\n=== DEBUG LOG FILE ===\n")
            f.write(f"Location: {self.debug_log_file}\n")
            
            if self.debug_log_file.exists():
                f.write(f"Size: {self.debug_log_file.stat().st_size} bytes\n")
                f.write(f"Last modified: {datetime.fromtimestamp(self.debug_log_file.stat().st_mtime)}\n")
        
        self.debug_logger.info(f"Debug report exported to: {report_path}")
        return str(report_path)

# Global debug handler instance
debug_handler = GUIDebugHandler()

# Convenience decorators
def debug_button(button_name: str, panel_name: str = "Unknown"):
    """Decorator for debugging button clicks."""
    return debug_handler.debug_button_click(button_name, panel_name)

def debug_operation(operation_name: str, panel_name: str = "Unknown"):
    """Decorator for debugging operations."""
    return debug_handler.debug_operation(operation_name, panel_name) 