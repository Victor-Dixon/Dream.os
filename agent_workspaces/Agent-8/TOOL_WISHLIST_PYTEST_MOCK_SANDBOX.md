# Tool Wishlist: Pytest Mock Sandbox for Filesystem Operations

**Goal:** Provide a safe, deterministic sandbox for filesystem-heavy pytest scenarios where `os.makedirs`, `os.path.join`, and path rewrites are heavily mocked. Prevents brittle mocks that block real directory creation while still validating paths.

## Problem
- Mocked `os.makedirs` and `os.path.join` in tests prevent real directories from being created, causing `FileNotFoundError` when writing artifacts (e.g., proof_ledger proofs).
- Tests need to assert normalized paths without breaking actual disk writes.
- Repeated re-implementation of mock helpers across tests increases flakiness and maintenance.

## Proposed Capabilities
- `sandbox_path(join_segments: list[str]) -> Path`: Deterministic path builder rooted in a temp sandbox; mirrors `os.path.join` semantics.
- `safe_makedirs(path: Path, *, allow_real: bool = True)`: Wrapper that always creates directories inside sandbox, even when mocks are active; no-op outside sandbox when `allow_real=False`.
- `with_mocked_fs(tmp_path)` context/fixture: Provides monkeypatched `os.path.join`, `os.makedirs`, and `open` (optionally) that forward to sandbox-safe implementations while still persisting files.
- Assertions helpers:
  - `assert_exists(path: Path)`: Asserts path exists in sandbox.
  - `assert_written(path: Path, matcher: Callable[[str], bool])`: Asserts file contents match predicate.
- Logging hook: emit debug logs of path rewrites and directory creations to aid triage.

## Usage Sketch (pytest fixture)
```python
@pytest.fixture
def mock_fs(tmp_path, pytest_mock_sandbox):
    with pytest_mock_sandbox(tmp_path) as sandbox:
        yield sandbox

def test_writes_file(mock_fs):
    proof_path = my_func_that_writes_file(mock_fs.join("quality", "proofs", "tdd"))
    mock_fs.assert_exists(proof_path)
```

## Deliverables
- Reusable helper module (e.g., `tests/utils/pytest_mock_sandbox.py`).
- Pytest fixture wiring for easy adoption across suites.
- Documentation and examples for common patterns (path rewrites, makedirs, open).
- Optional strict mode to fail on writes outside sandbox.

## Benefits
- Eliminates brittle `os.makedirs` mocks that block real writes.
- Reduces duplicated mocking code across tests.
- Improves debuggability with structured logs.
- Safer, deterministic filesystem behavior in tests.

