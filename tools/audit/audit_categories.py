import os
import subprocess
import sys
from pathlib import Path

def audit_tool(tool_path: Path):
    try:
        result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return "PASS"
        if "unrecognized arguments: --help" in result.stderr or "invalid choice: '--help'" in result.stderr:
            return "PASS"
        err = result.stderr[:100].replace('\n', ' ')
        return "FAIL: " + err
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return "ERROR: " + str(e)

def main():
    cat_dir = Path("tools/categories")
    for root, dirs, files in os.walk(cat_dir):
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                p = Path(root) / f
                res = audit_tool(p)
                if "PASS" not in res:
                    print(f"{p}: {res}")

if __name__ == "__main__":
    main()
