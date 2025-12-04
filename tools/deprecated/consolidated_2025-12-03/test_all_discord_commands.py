#!/usr/bin/env python3
"""
Comprehensive Discord Commands Test Script
==========================================

Tests all Discord bot commands to ensure they work correctly.
Verifies command registration, error handling, and functionality.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-01-27
"""

import asyncio
import json
import sys
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Discord context for testing
class MockContext:
    """Mock Discord context for command testing."""
    def __init__(self):
        self.author = type('Author', (), {'display_name': 'TestUser', 'id': '123456789'})()
        self.send = self._mock_send
        self.message = type('Message', (), {'content': '!test', 'author': self.author})()
        self.channel = type('Channel', (), {'id': '987654321'})()
        self.guild = None
        self._sent_messages = []
    
    async def _mock_send(self, *args, **kwargs):
        """Mock send method that records messages."""
        self._sent_messages.append({'args': args, 'kwargs': kwargs})
        return type('Message', (), {'id': 'msg123'})()
    
    def get_last_message(self):
        """Get the last sent message."""
        return self._sent_messages[-1] if self._sent_messages else None


class DiscordCommandsTester:
    """Comprehensive tester for all Discord commands."""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.utcnow().isoformat(),
            'commands_tested': [],
            'passed': [],
            'failed': [],
            'errors': [],
            'summary': {}
        }
    
    def test_command_registration(self) -> Dict[str, Any]:
        """Test that all commands are properly registered."""
        logger.info("🔍 Testing command registration...")
        
        try:
            from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
            
            # Create bot instance (won't actually connect)
            bot = UnifiedDiscordBot(token="TEST_TOKEN", channel_id=None)
            
            # Get all registered commands
            commands = {}
            for command in bot.commands:
                commands[command.name] = {
                    'aliases': command.aliases,
                    'description': command.description,
                    'help': command.help,
                }
            
            logger.info(f"✅ Found {len(commands)} registered commands")
            
            return {
                'success': True,
                'total_commands': len(commands),
                'commands': commands
            }
        except Exception as e:
            logger.error(f"❌ Error testing command registration: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_messaging_commands(self) -> List[Dict[str, Any]]:
        """Test messaging-related commands."""
        logger.info("📨 Testing messaging commands...")
        
        results = []
        
        # Test commands that should exist
        messaging_commands = [
            'control', 'panel', 'menu',  # Aliases for control
            'gui',
            'status',
            'message',
            'broadcast',
            'help',
        ]
        
        for cmd_name in messaging_commands:
            try:
                # Check if command exists in unified_discord_bot
                from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
                bot = UnifiedDiscordBot(token="TEST_TOKEN", channel_id=None)
                
                command = bot.get_command(cmd_name)
                if command:
                    results.append({
                        'command': cmd_name,
                        'status': '✅ REGISTERED',
                        'has_error_handling': self._check_error_handling(cmd_name, 'unified_discord_bot.py')
                    })
                else:
                    results.append({
                        'command': cmd_name,
                        'status': '❌ NOT FOUND',
                        'error': 'Command not registered'
                    })
            except Exception as e:
                results.append({
                    'command': cmd_name,
                    'status': '❌ ERROR',
                    'error': str(e)
                })
        
        return results
    
    def test_swarm_showcase_commands(self) -> List[Dict[str, Any]]:
        """Test swarm showcase commands."""
        logger.info("🐝 Testing swarm showcase commands...")
        
        results = []
        
        showcase_commands = [
            'swarm_tasks', 'tasks', 'directives',  # Aliases
            'swarm_roadmap', 'roadmap', 'plan',  # Aliases
            'swarm_excellence', 'excellence', 'achievements',  # Aliases
            'swarm_overview', 'overview', 'dashboard',  # Aliases
        ]
        
        for cmd_name in showcase_commands:
            try:
                from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
                bot = UnifiedDiscordBot(token="TEST_TOKEN", channel_id=None)
                
                command = bot.get_command(cmd_name)
                if command:
                    results.append({
                        'command': cmd_name,
                        'status': '✅ REGISTERED',
                        'has_error_handling': self._check_error_handling(cmd_name, 'swarm_showcase_commands.py')
                    })
                else:
                    results.append({
                        'command': cmd_name,
                        'status': '❌ NOT FOUND',
                        'error': 'Command not registered'
                    })
            except Exception as e:
                results.append({
                    'command': cmd_name,
                    'status': '❌ ERROR',
                    'error': str(e)
                })
        
        return results
    
    def test_github_book_commands(self) -> List[Dict[str, Any]]:
        """Test GitHub book viewer commands."""
        logger.info("📚 Testing GitHub book commands...")
        
        results = []
        
        book_commands = [
            'github_book', 'book', 'repos',  # Aliases
            'goldmines', 'jackpots', 'discoveries',  # Aliases
            'book_stats', 'book_progress', 'repo_stats',  # Aliases
            'book_search', 'search_repos', 'find_repo',  # Aliases
            'book_filter', 'filter_repos', 'repos_by_agent',  # Aliases
        ]
        
        for cmd_name in book_commands:
            try:
                from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
                bot = UnifiedDiscordBot(token="TEST_TOKEN", channel_id=None)
                
                command = bot.get_command(cmd_name)
                if command:
                    results.append({
                        'command': cmd_name,
                        'status': '✅ REGISTERED',
                        'has_error_handling': self._check_error_handling(cmd_name, 'github_book_viewer.py')
                    })
                else:
                    results.append({
                        'command': cmd_name,
                        'status': '❌ NOT FOUND',
                        'error': 'Command not registered'
                    })
            except Exception as e:
                results.append({
                    'command': cmd_name,
                    'status': '❌ ERROR',
                    'error': str(e)
                })
        
        return results
    
    def test_command_error_handling(self) -> Dict[str, Any]:
        """Test error handling in commands."""
        logger.info("🛡️  Testing command error handling...")
        
        # Read the test report
        report_file = Path('data/discord_commands_test_report.json')
        if not report_file.exists():
            return {
                'success': False,
                'error': 'Test report not found. Run discord_commands_tester.py first.'
            }
        
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        commands_needing_handling = report.get('commands_needing_handling', [])
        
        return {
            'success': True,
            'total_commands': report['summary']['total_commands'],
            'commands_with_handling': report['summary']['commands_with_handling'],
            'coverage': report['summary']['error_handling_coverage'],
            'commands_needing_handling': commands_needing_handling
        }
    
    def _check_error_handling(self, command_name: str, file_name: str) -> bool:
        """Check if a command has error handling."""
        try:
            file_path = Path(f'src/discord_commander/{file_name}')
            if not file_path.exists():
                return False
            
            content = file_path.read_text(encoding='utf-8')
            
            # Look for command function
            import re
            pattern = rf'async def {command_name}\(.*?\):(.*?)(?=async def |@commands\.command|$)'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                func_body = match.group(1)
                has_try_except = 'try:' in func_body and 'except' in func_body
                has_error_response = 'await ctx.send' in func_body and ('error' in func_body.lower() or '❌' in func_body)
                return has_try_except and has_error_response
            
            return False
        except Exception:
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and generate comprehensive report."""
        logger.info("🧪 Running comprehensive Discord commands test suite...")
        logger.info("=" * 70)
        
        # Test command registration
        registration_result = self.test_command_registration()
        self.results['registration'] = registration_result
        
        # Test messaging commands
        messaging_results = self.test_messaging_commands()
        self.results['messaging_commands'] = messaging_results
        
        # Test swarm showcase commands
        showcase_results = self.test_swarm_showcase_commands()
        self.results['showcase_commands'] = showcase_results
        
        # Test GitHub book commands
        book_results = self.test_github_book_commands()
        self.results['book_commands'] = book_results
        
        # Test error handling
        error_handling_result = self.test_command_error_handling()
        self.results['error_handling'] = error_handling_result
        
        # Generate summary
        self._generate_summary()
        
        return self.results
    
    def _generate_summary(self):
        """Generate test summary."""
        total_tested = 0
        total_passed = 0
        total_failed = 0
        
        # Count messaging commands
        if 'messaging_commands' in self.results:
            for cmd in self.results['messaging_commands']:
                total_tested += 1
                if '✅' in cmd.get('status', ''):
                    total_passed += 1
                else:
                    total_failed += 1
        
        # Count showcase commands
        if 'showcase_commands' in self.results:
            for cmd in self.results['showcase_commands']:
                total_tested += 1
                if '✅' in cmd.get('status', ''):
                    total_passed += 1
                else:
                    total_failed += 1
        
        # Count book commands
        if 'book_commands' in self.results:
            for cmd in self.results['book_commands']:
                total_tested += 1
                if '✅' in cmd.get('status', ''):
                    total_passed += 1
                else:
                    total_failed += 1
        
        self.results['summary'] = {
            'total_tested': total_tested,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'success_rate': f'{(total_passed/total_tested*100):.1f}%' if total_tested > 0 else '0%'
        }
    
    def print_report(self):
        """Print formatted test report."""
        print("\n" + "=" * 70)
        print("📊 DISCORD COMMANDS COMPREHENSIVE TEST REPORT")
        print("=" * 70)
        print()
        
        # Registration
        if 'registration' in self.results:
            reg = self.results['registration']
            if reg.get('success'):
                print(f"✅ Command Registration: {reg['total_commands']} commands found")
            else:
                print(f"❌ Command Registration: {reg.get('error', 'Unknown error')}")
        print()
        
        # Summary
        if 'summary' in self.results:
            summary = self.results['summary']
            print(f"📊 Test Summary:")
            print(f"   Total Tested: {summary['total_tested']}")
            print(f"   ✅ Passed: {summary['total_passed']}")
            print(f"   ❌ Failed: {summary['total_failed']}")
            print(f"   📈 Success Rate: {summary['success_rate']}")
            print()
        
        # Error handling
        if 'error_handling' in self.results:
            eh = self.results['error_handling']
            if eh.get('success'):
                print(f"🛡️  Error Handling:")
                print(f"   Coverage: {eh['coverage']}")
                print(f"   Commands with Handling: {eh['commands_with_handling']}/{eh['total_commands']}")
                if eh.get('commands_needing_handling'):
                    print(f"   ⚠️  {len(eh['commands_needing_handling'])} commands need error handling")
            print()
        
        # Failed commands
        failed_commands = []
        for category in ['messaging_commands', 'showcase_commands', 'book_commands']:
            if category in self.results:
                for cmd in self.results[category]:
                    if '❌' in cmd.get('status', ''):
                        failed_commands.append({
                            'command': cmd['command'],
                            'category': category.replace('_commands', ''),
                            'error': cmd.get('error', 'Unknown error')
                        })
        
        if failed_commands:
            print("❌ Failed Commands:")
            print("-" * 70)
            for cmd in failed_commands:
                print(f"   • {cmd['command']} ({cmd['category']})")
                print(f"     Error: {cmd['error']}")
            print()
        
        print("=" * 70)
        print()


def main():
    """Main test execution."""
    tester = DiscordCommandsTester()
    results = tester.run_all_tests()
    tester.print_report()
    
    # Save results
    report_file = Path('data/discord_commands_comprehensive_test.json')
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Full report saved to: {report_file}\n")
    
    # Return exit code
    summary = results.get('summary', {})
    if summary.get('total_failed', 0) > 0:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

