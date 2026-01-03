# -------------------------------------------------------------------
# File Path: C:\Projects\AI_Debugger_Assistant\src\error_detection\error_detection.py
#
# Project: AI_Debugger_Assistant
#
# Description:
# This file is part of the AI_Debugger_Assistant project.
# It provides tools to detect syntax, runtime, and logic errors within 
# Python code using various methods, including Python's built-in `exec`, 
# subprocess calls for static analysis tools, and custom error handling.
# The results provide detailed feedback on code issues for debugging 
# assistance and error correction.
#
# Classes:
# - ErrorDetector: Handles detection of syntax, runtime, and logic errors 
#   within provided code.
#
# Usage:
# The `ErrorDetector` class is designed to be instantiated with a code 
# snippet, providing methods to identify and classify different error types.
# -------------------------------------------------------------------

import ast
import subprocess
import tempfile
import traceback
import os
import logging

# Configure logging
logging.basicConfig(
    filename='error_detection.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ErrorDetector:
    """
    Class for detecting and classifying errors in Python code.
    Supports syntax error detection, runtime error handling, 
    and logic error identification through static analysis.
    """

    def __init__(self, code: str):
        """
        Initializes the ErrorDetector with code for analysis.
        
        Args:
            code (str): Python code to be analyzed.
        """
        self.code = code

    def detect_syntax_errors(self) -> str:
        """
        Detects syntax errors in the provided code using AST parsing.

        Returns:
            str: Description of syntax errors if found, or an empty string.
        """
        try:
            ast.parse(self.code)
            return ""
        except SyntaxError as e:
            suggested_fix = self.suggest_fix(e)
            error_message = f"Syntax Error: {e.msg} (line {e.lineno})\nSuggested Fix: {suggested_fix}"
            logging.error(error_message)
            return error_message

    def suggest_fix(self, error: SyntaxError) -> str:
        """
        Suggests a potential fix for syntax errors.
        
        Args:
            error (SyntaxError): The syntax error encountered.
        
        Returns:
            str: Suggested fix for the syntax error.
        """
        if "expected ':'" in error.msg:
            return "Check for missing ':' at the end of the line."
        elif "unexpected EOF while parsing" in error.msg:
            return "Ensure all code blocks (loops, functions) are properly closed."
        return "Refer to Python syntax documentation for valid syntax."

    def detect_runtime_errors(self, globals_=None, locals_=None) -> str:
        """
        Detects runtime errors by executing the code in a controlled environment.
        
        Args:
            globals_ (dict): Optional globals for code execution.
            locals_ (dict): Optional locals for code execution.

        Returns:
            str: Description of runtime errors if found, or an empty string.
        """
        try:
            exec(self.code, globals_ or {}, locals_ or {})
            return ""
        except Exception as e:
            error_message = f"Runtime Error: {str(e)}\n" + traceback.format_exc()
            logging.error(error_message)
            return error_message

    def detect_logic_errors(self) -> str:
        """
        Detects potential logic errors using static analysis with pylint.

        Returns:
            str: Output of pylint analysis indicating logic issues.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
            tmp_file.write(self.code.encode("utf-8"))
            tmp_file_path = tmp_file.name

        try:
            result = subprocess.run(
                ["pylint", tmp_file_path, "--disable=C,R,W"],
                capture_output=True,
                text=True,
                check=True
            )
            categorized_issues = self.categorize_logic_errors(result.stdout)
            logging.warning(f"Logic Errors Detected:\n{categorized_issues}")
            return categorized_issues
        except subprocess.CalledProcessError as e:
            return f"Logic Error: {e.output.strip()}"
        finally:
            os.remove(tmp_file_path)

    def categorize_logic_errors(self, pylint_output: str) -> str:
        """
        Categorizes logic errors by severity based on pylint output.
        
        Args:
            pylint_output (str): Raw pylint output.
        
        Returns:
            str: Categorized logic errors.
        """
        major_issues = []
        minor_issues = []
        for line in pylint_output.split('\n'):
            if "error" in line.lower():
                major_issues.append(line)
            elif "warning" in line.lower():
                minor_issues.append(line)
        
        categorized_output = "Major Issues:\n" + '\n'.join(major_issues) + "\nMinor Issues:\n" + '\n'.join(minor_issues)
        return categorized_output

    def detect_all_errors(self) -> dict:
        """
        Detects all error types: syntax, runtime, and logic.

        Returns:
            dict: Dictionary of error types and their descriptions.
        """
        errors = {
            "syntax_errors": self.detect_syntax_errors(),
            "runtime_errors": self.detect_runtime_errors(),
            "logic_errors": self.detect_logic_errors()
        }
        return errors

# Example Usage:
if __name__ == "__main__":
    code_snippet = """
for i in range(10)
    print(i)
"""
    detector = ErrorDetector(code_snippet)
    all_errors = detector.detect_all_errors()
    print("Syntax Errors:", all_errors["syntax_errors"])
    print("Runtime Errors:", all_errors["runtime_errors"])
    print("Logic Errors:", all_errors["logic_errors"])

# -------------------------------------------------------------------
# Enhancements Implemented
# -------------------------------------------------------------------
# 1. **Automated Error Correction Suggestions**: Provides fixes for common
#    syntax errors such as missing colons and unexpected EOF.
#
# 2. **Logic Error Categorization**: Separates logic errors into major 
#    and minor categories based on pylint output.
#
# 3. **Error Logging**: Logs syntax, runtime, and logic errors into 
#    `error_detection.log` for tracking and debugging purposes.
# -------------------------------------------------------------------
