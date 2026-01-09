#!/usr/bin/env python3
"""
Test Thea Communication and Collect Response
"""

from src.services.thea.di_container import TheaDIContainer
import json
from datetime import datetime

print('🧪 Testing Thea Communication - Collecting Real Response')
print('=' * 60)

try:
    container = TheaDIContainer()
    coordinator = container.coordinator

    # Send a comprehensive test message about the project using Thea custom GPT
    test_message = '''Please analyze this V2 Compliance project and provide a summary of what has been accomplished:

Key areas to cover:
1. Modular Thea Service Architecture - What was refactored?
2. Mock Removal - What simulated components were replaced with real implementations?
3. Consolidation Automation - What automation was implemented?
4. Authentication & Security - How is Thea now properly secured?
5. GUI Integration - What real Thea functionality was added to the interface?

Please provide a concise but comprehensive summary suitable for a project README or documentation.'''

    print('📤 Sending message to Thea...')
    result = coordinator.send_message(test_message)

    print('📊 Communication Result:')
    status = "✅ SUCCESS" if result.success else "❌ FAILED"
    print(f'   Status: {status}')
    print(f'   Duration: {result.duration_seconds:.2f} seconds')

    if result.success and result.response:
        print(f'   Response Length: {len(result.response.content)} characters')
        print('\n🤖 Thea Response:\n')
        print(result.response.content)

        # Save the response for documentation
        response_data = {
            'timestamp': datetime.now().isoformat(),
            'message': test_message,
            'response': result.response.content,
            'duration_seconds': result.duration_seconds,
            'success': result.success
        }

        with open('thea_project_analysis_response.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)

        print('\n💾 Response saved to: thea_project_analysis_response.json')

    else:
        print(f'   Error: {result.error_message}')

except Exception as e:
    print(f'❌ Test failed with exception: {e}')
    import traceback
    traceback.print_exc()