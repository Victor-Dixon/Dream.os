"""
Job Queue for DreamVault AI Training Pipeline
============================================

SSOT Domain: ai_training

V2 Compliant: <120 lines, single responsibility
Asynchronous job queue for AI training operations.
"""

import asyncio
import threading
from typing import Any, List, Optional, Callable, Dict
from dataclasses import dataclass
from enum import Enum
import time


class JobStatus(Enum):
    """Job status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Job representation"""
    id: str
    task: Callable
    args: tuple = ()
    kwargs: dict = None
    priority: int = 0
    status: JobStatus = JobStatus.PENDING
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
        if self.created_at is None:
            self.created_at = time.time()


class JobQueue:
    """
    V2 Compliant Job Queue

    Asynchronous job processing for AI training operations.
    Single responsibility: job queuing and execution.
    """

    def __init__(self, max_workers: int = 4, max_queue_size: int = 1000):
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size

        # Thread safety
        self._lock = threading.Lock()
        self._shutdown_event = threading.Event()

        # Job storage
        self._pending_jobs: List[Job] = []
        self._running_jobs: Dict[str, Job] = {}
        self._completed_jobs: Dict[str, Job] = {}

        # Worker management
        self._workers: List[threading.Thread] = []
        self._semaphore = threading.Semaphore(max_workers)

        # Callbacks
        self._job_callbacks: Dict[str, List[Callable]] = {}

        # Start workers
        self._start_workers()

    def submit_job(self, job_id: str, task: Callable, *args, priority: int = 0, **kwargs) -> bool:
        """
        Submit a job to the queue.

        Args:
            job_id: Unique job identifier
            task: Callable to execute
            priority: Job priority (higher = more important)
            *args, **kwargs: Arguments for the task

        Returns:
            True if job was submitted, False if queue is full
        """
        with self._lock:
            if len(self._pending_jobs) >= self.max_queue_size:
                return False

            job = Job(
                id=job_id,
                task=task,
                args=args,
                kwargs=kwargs,
                priority=priority
            )

            self._pending_jobs.append(job)
            self._pending_jobs.sort(key=lambda j: (-j.priority, j.created_at))

            return True

    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a pending job.

        Args:
            job_id: Job identifier

        Returns:
            True if job was cancelled, False if not found or already running
        """
        with self._lock:
            for i, job in enumerate(self._pending_jobs):
                if job.id == job_id:
                    job.status = JobStatus.CANCELLED
                    self._pending_jobs.pop(i)
                    return True

            return False

    def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        """Get status of a job."""
        with self._lock:
            if job_id in self._running_jobs:
                return self._running_jobs[job_id].status
            if job_id in self._completed_jobs:
                return self._completed_jobs[job_id].status

            for job in self._pending_jobs:
                if job.id == job_id:
                    return job.status

            return None

    def get_job_result(self, job_id: str) -> Optional[Any]:
        """Get result of a completed job."""
        with self._lock:
            if job_id in self._completed_jobs:
                job = self._completed_jobs[job_id]
                return {"result": job.result, "error": job.error, "status": job.status}

            return None

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        with self._lock:
            return {
                "pending_jobs": len(self._pending_jobs),
                "running_jobs": len(self._running_jobs),
                "completed_jobs": len(self._completed_jobs),
                "max_queue_size": self.max_queue_size,
                "active_workers": len([w for w in self._workers if w.is_alive()])
            }

    def add_job_callback(self, job_id: str, callback: Callable) -> None:
        """Add callback for job completion."""
        with self._lock:
            if job_id not in self._job_callbacks:
                self._job_callbacks[job_id] = []
            self._job_callbacks[job_id].append(callback)

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the job queue."""
        self._shutdown_event.set()

        if wait:
            for worker in self._workers:
                worker.join(timeout=5)

    def _start_workers(self) -> None:
        """Start worker threads."""
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"JobWorker-{i}",
                daemon=True
            )
            worker.start()
            self._workers.append(worker)

    def _worker_loop(self) -> None:
        """Main worker loop."""
        while not self._shutdown_event.is_set():
            self._semaphore.acquire()

            try:
                job = None
                with self._lock:
                    if self._pending_jobs:
                        job = self._pending_jobs.pop(0)
                        job.status = JobStatus.RUNNING
                        job.started_at = time.time()
                        self._running_jobs[job.id] = job

                if job:
                    try:
                        result = job.task(*job.args, **job.kwargs)
                        job.result = result
                        job.status = JobStatus.COMPLETED
                    except Exception as e:
                        job.error = str(e)
                        job.status = JobStatus.FAILED
                    finally:
                        job.completed_at = time.time()

                        with self._lock:
                            if job.id in self._running_jobs:
                                del self._running_jobs[job.id]
                            self._completed_jobs[job.id] = job

                            # Trigger callbacks
                            if job.id in self._job_callbacks:
                                for callback in self._job_callbacks[job.id]:
                                    try:
                                        callback(job)
                                    except Exception as e:
                                        print(f"Callback error: {e}")

            finally:
                self._semaphore.release()

            # Small delay to prevent busy waiting
            time.sleep(0.01)