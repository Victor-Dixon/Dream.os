"""AI Context Engine entrypoint."""

import asyncio

from .session_manager import SessionManager


async def main() -> None:
    """Run a minimal session manager lifecycle."""
    manager = SessionManager()
    await manager.start_background_tasks()
    await manager.stop_background_tasks()


if __name__ == "__main__":
    asyncio.run(main())
