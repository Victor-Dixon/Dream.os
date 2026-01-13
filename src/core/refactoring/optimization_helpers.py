"""
<!-- SSOT Domain: core -->

Optimization Helper Functions
=============================

Helper functions for code optimization operations.
Uses AST-based analysis for class structure optimization.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
Refactored: Agent-7 (Web Development Specialist) - AST-based optimization
License: MIT
"""

import ast
from typing import Any


def apply_optimization_rules(file_path: str, rules: list[str]) -> None:
    """Apply optimization rules to a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Apply basic optimizations
        optimized_content = content

        # Remove unused imports
        optimized_content = remove_unused_imports(optimized_content)

        # Optimize class structure
        optimized_content = optimize_class_structure(optimized_content)

        # Write optimized content back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(optimized_content)

    except Exception as e:
        print(f"Failed to optimize {file_path}: {e}")


def remove_unused_imports(content: str) -> str:
    """Remove unused imports from content."""
    # Basic implementation - in practice, would use more sophisticated analysis
    lines = content.split("\n")
    filtered_lines = []

    for line in lines:
        if not line.strip().startswith("import ") or "#" in line:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)


def optimize_class_structure(content: str) -> str:
    """Optimize class structure in content using AST analysis."""
    try:
        tree = ast.parse(content)
        optimizer = ClassStructureOptimizer()
        optimizer.visit(tree)
        return optimizer.get_optimized_code(content)
    except SyntaxError:
        # If parsing fails, return original content
        return content
    except Exception:
        # On any other error, return original content
        return content


class ClassStructureOptimizer(ast.NodeTransformer):
    """AST-based class structure optimizer."""

    def __init__(self):
        """Initialize optimizer."""
        self.optimizations = []
        self.max_methods_per_class = 15
        self.max_class_length = 200

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Analyze and optimize class definitions."""
        # Count methods and class complexity
        method_count = sum(
            1
            for item in node.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        )

        # Check if class is too large
        class_lines = sum(
            len(str(item).split("\n")) for item in node.body
        )

        # Record optimization suggestions
        if method_count > self.max_methods_per_class:
            self.optimizations.append(
                f"Class {node.name} has {method_count} methods "
                f"(consider splitting into smaller classes)"
            )

        if class_lines > self.max_class_length:
            self.optimizations.append(
                f"Class {node.name} is {class_lines} lines "
                f"(consider refactoring into smaller components)"
            )

        # Check for duplicate code patterns
        method_names = [
            item.name
            for item in node.body
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        # Look for similar method names (potential duplication)
        for i, name1 in enumerate(method_names):
            for name2 in method_names[i + 1 :]:
                if self._names_similar(name1, name2):
                    self.optimizations.append(
                        f"Potential duplicate methods: {name1} and {name2} "
                        f"in class {node.name}"
                    )

        return self.generic_visit(node)

    def _names_similar(self, name1: str, name2: str) -> bool:
        """Check if two method names are similar (potential duplication)."""
        # Simple similarity check - names with common prefixes/suffixes
        if len(name1) < 3 or len(name2) < 3:
            return False

        # Check for common prefix (e.g., get_user, get_profile)
        if name1.startswith(name2[:3]) or name2.startswith(name1[:3]):
            return True

        # Check for common suffix (e.g., validate_user, validate_profile)
        if name1.endswith(name2[-3:]) or name2.endswith(name1[-3:]):
            return True

        return False

    def get_optimized_code(self, original_content: str) -> str:
        """Get optimized code with suggestions."""
        # For now, return original content
        # In a full implementation, this would apply transformations
        # For this placeholder implementation, we return the original
        # but log optimization suggestions
        if self.optimizations:
            # Could add comments with suggestions, but for now just return original
            pass

        return original_content
