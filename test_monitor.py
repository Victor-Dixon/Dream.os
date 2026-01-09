#!/usr/bin/env python3
import asyncio
import sys
sys.path.insert(0, 'src')
from services.repository_monitor import repository_monitor

async def test():
    print("Testing repository monitor...")
    print(f"Repository path: {repository_monitor.repository_path}")
    print(f"Monitoring active: {repository_monitor.is_monitoring}")

    # Trigger a scan
    print("Running initial scan...")
    await repository_monitor._perform_scan()

    stats = repository_monitor.get_current_stats()
    print(f"Found {stats.get('total_files', 0)} files, {stats.get('total_size_mb', 0):.1f} MB")
    print(f"Snapshots: {len(repository_monitor.snapshots)}")
    print("Repository monitor initialized successfully!")

asyncio.run(test())