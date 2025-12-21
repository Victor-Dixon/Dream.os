"""Quick script to check all tools for syntax errors."""
import ast
from pathlib import Path

tools_dir = Path(__file__).parent
errors = []

for py_file in tools_dir.rglob('*.py'):
    if any(x in str(py_file) for x in ['__pycache__', '.pyc', 'test_', '_test.py', 'archive', 'deprecated', '__init__.py', 'check_all_syntax_errors.py', 'classify_all_tools_phase1.py', 'fix_syntax_errors_phase0.py']):
        continue
    
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
    except SyntaxError as e:
        errors.append((str(py_file.relative_to(tools_dir.parent)), e.lineno, str(e)))
    except Exception as e:
        errors.append((str(py_file.relative_to(tools_dir.parent)), None, f"Read error: {str(e)}"))

print(f"Found {len(errors)} syntax errors:")
for file, line, msg in errors[:20]:
    print(f"  {file}:{line} - {msg[:60]}")

