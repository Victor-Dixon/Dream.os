#!/usr/bin/env python3
"""
Twitch Bot Health Monitor
=========================

Monitors Twitch bot connection health, verifies PING/PONG handling,
and provides real-time status updates.

Usage:
    python tools/twitch_bot_health_monitor.py [--watch] [--duration SECONDS]

Features:
    - Pre-flight configuration check
    - Connection stability test
    - PING/PONG activity monitoring
    - Automatic reconnection detection
    - Health status reporting
"""

import asyncio
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class TwitchBotHealthMonitor:
    """Monitor Twitch bot connection health."""
    
    def __init__(self):
        self.channel = os.getenv("TWITCH_CHANNEL")
        self.token = os.getenv("TWITCH_ACCESS_TOKEN")
        self.username = os.getenv("TWITCH_BOT_USERNAME") or self.channel
        self.bridge = None
        self.ping_count = 0
        self.pong_count = 0
        self.disconnect_count = 0
        self.start_time = None
        self.last_ping_time = None
        self.last_pong_time = None
        
    def check_config(self) -> bool:
        """Check if configuration is valid."""
        print("=" * 60)
        print("🔍 CONFIGURATION CHECK")
        print("=" * 60)
        
        issues = []
        
        if not self.channel:
            issues.append("❌ TWITCH_CHANNEL not set")
        else:
            print(f"✅ Channel: {self.channel}")
        
        if not self.token:
            issues.append("❌ TWITCH_ACCESS_TOKEN not set")
        else:
            token_preview = self.token[:20] + "..." if len(self.token) > 20 else self.token
            print(f"✅ Token: {token_preview}")
            if not self.token.startswith("oauth:"):
                issues.append("⚠️ Token should start with 'oauth:'")
        
        if not self.username:
            issues.append("❌ TWITCH_BOT_USERNAME not set (using channel name)")
        else:
            print(f"✅ Username: {self.username}")
        
        if issues:
            print("\n❌ Configuration Issues:")
            for issue in issues:
                print(f"   {issue}")
            return False
        
        print("\n✅ Configuration valid!")
        return True
    
    async def monitor_connection(self, duration: int = 60) -> dict:
        """
        Monitor bot connection for specified duration.
        
        Args:
            duration: Seconds to monitor (default: 60)
            
        Returns:
            Health report dictionary
        """
        if not self.check_config():
            return {"status": "failed", "reason": "configuration_invalid"}
        
        print("\n" + "=" * 60)
        print("🏥 STARTING HEALTH MONITOR")
        print("=" * 60)
        print(f"⏱️  Monitoring for {duration} seconds...")
        print()
        
        try:
            from src.services.chat_presence.twitch_bridge import TwitchChatBridge
            
            # Create bridge with enhanced message handler
            self.bridge = TwitchChatBridge(
                username=self.username,
                oauth_token=self.token,
                channel=self.channel,
                on_message=self._handle_message,
            )
            
            # Patch the bot's on_ping handler to track PINGs
            original_on_ping = None
            if hasattr(self.bridge.bot, 'on_ping'):
                original_on_ping = self.bridge.bot.on_ping
            
            def tracked_on_ping(connection, event):
                self.ping_count += 1
                self.last_ping_time = time.time()
                print(f"🏓 [{datetime.now().strftime('%H:%M:%S')}] PING #{self.ping_count} received")
                if original_on_ping:
                    original_on_ping(connection, event)
                else:
                    # Fallback PONG if handler missing
                    try:
                        server_name = ""
                        if hasattr(event, 'arguments') and event.arguments:
                            server_name = event.arguments[0] if len(event.arguments) > 0 else ""
                        elif hasattr(event, 'target') and event.target:
                            server_name = event.target
                        else:
                            server_name = "tmi.twitch.tv"
                        connection.pong(server_name)
                        self.pong_count += 1
                        self.last_pong_time = time.time()
                        print(f"🏓 [{datetime.now().strftime('%H:%M:%S')}] PONG #{self.pong_count} sent")
                    except Exception as e:
                        print(f"❌ Failed to send PONG: {e}")
            
            # Connect
            print("🔌 Connecting to Twitch...")
            connected = await self.bridge.connect()
            
            if not connected:
                return {
                    "status": "failed",
                    "reason": "connection_failed",
                    "ping_count": 0,
                    "pong_count": 0,
                }
            
            self.start_time = time.time()
            print("✅ Connection initiated")
            print()
            print("📊 Monitoring connection health...")
            print("   (Watch for PING/PONG activity)")
            print()
            
            # Monitor for duration
            check_interval = 5  # Check every 5 seconds
            checks = duration // check_interval
            
            for i in range(checks):
                await asyncio.sleep(check_interval)
                elapsed = int(time.time() - self.start_time)
                
                # Status line
                status_icon = "✅" if self.bridge.running and self.bridge.connected else "⚠️"
                running_status = "Running" if self.bridge.running else "Stopped"
                connected_status = "Connected" if self.bridge.connected else "Disconnected"
                
                print(f"[{elapsed:3d}s] {status_icon} {running_status} | {connected_status} | "
                      f"PING: {self.ping_count} | PONG: {self.pong_count}")
                
                # Check for disconnection
                if not self.bridge.running:
                    self.disconnect_count += 1
                    print(f"⚠️ [{datetime.now().strftime('%H:%M:%S')}] Connection lost!")
                    break
            
            # Final report
            total_time = time.time() - self.start_time
            
            report = {
                "status": "success" if self.bridge.running and self.bridge.connected else "disconnected",
                "duration": int(total_time),
                "ping_count": self.ping_count,
                "pong_count": self.pong_count,
                "disconnect_count": self.disconnect_count,
                "running": self.bridge.running,
                "connected": self.bridge.connected,
            }
            
            return report
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "ping_count": self.ping_count,
                "pong_count": self.pong_count,
            }
        finally:
            if self.bridge:
                print("\n🛑 Stopping bot...")
                self.bridge.stop()
    
    def _handle_message(self, message_data: dict) -> None:
        """Handle incoming messages (for testing)."""
        # Just acknowledge - don't spam logs
        pass
    
    def print_report(self, report: dict) -> None:
        """Print health report."""
        print("\n" + "=" * 60)
        print("📊 HEALTH REPORT")
        print("=" * 60)
        
        status = report.get("status", "unknown")
        status_icon = "✅" if status == "success" else "⚠️" if status == "disconnected" else "❌"
        
        print(f"\n{status_icon} Status: {status.upper()}")
        print(f"⏱️  Duration: {report.get('duration', 0)} seconds")
        print(f"🏓 PINGs received: {report.get('ping_count', 0)}")
        print(f"🏓 PONGs sent: {report.get('pong_count', 0)}")
        print(f"🔌 Disconnects: {report.get('disconnect_count', 0)}")
        print(f"🔄 Running: {report.get('running', False)}")
        print(f"✅ Connected: {report.get('connected', False)}")
        
        # Analysis
        print("\n📈 Analysis:")
        ping_count = report.get("ping_count", 0)
        pong_count = report.get("pong_count", 0)
        
        if ping_count == 0 and report.get("duration", 0) < 60:
            print("   ℹ️  No PINGs received (normal for short tests)")
        elif ping_count > 0 and pong_count == ping_count:
            print("   ✅ PING/PONG handling working correctly!")
        elif ping_count > pong_count:
            print("   ⚠️  WARNING: PINGs received but PONGs missing!")
            print("   ⚠️  This will cause disconnections!")
        elif pong_count > ping_count:
            print("   ⚠️  WARNING: More PONGs than PINGs (unusual)")
        
        if report.get("disconnect_count", 0) > 0:
            print("   ❌ Connection was lost during monitoring")
        elif report.get("status") == "success":
            print("   ✅ Connection stable throughout monitoring period")
        
        print()


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Twitch Bot Health Monitor")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch mode - monitor continuously until interrupted"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration to monitor in seconds (default: 60)"
    )
    
    args = parser.parse_args()
    
    monitor = TwitchBotHealthMonitor()
    
    if args.watch:
        print("🔄 WATCH MODE: Monitoring continuously (Ctrl+C to stop)")
        print()
        try:
            while True:
                report = await monitor.monitor_connection(duration=args.duration)
                monitor.print_report(report)
                print("⏳ Waiting 5 seconds before next check...")
                await asyncio.sleep(5)
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
    else:
        report = await monitor.monitor_connection(duration=args.duration)
        monitor.print_report(report)
        
        # Exit code based on status
        if report.get("status") == "success":
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
        sys.exit(130)

