# ResumeTracker shim for backward compatibility
try:
    from ..legacy.resume_tracker import ResumeTracker
except ImportError:
    # Fallback: define a dummy ResumeTracker
    class ResumeTracker:
        def __init__(self, *args, **kwargs):
            raise ImportError('ResumeTracker is not available. Please restore resume_tracker.py.') 