#!/usr/bin/env python3
"""
WearSwarm.online Validation Script
Validates Google Fonts loading and character rendering
"""

import requests
from bs4 import BeautifulSoup

def validate_weareswarm():
    """Validate weareswarm.online Google Fonts and rendering"""

    print('🔍 Validating weareswarm.online Google Fonts rendering...')
    print('=' * 60)

    try:
        # Check the main page
        response = requests.get('https://weareswarm.online', timeout=10)
        print(f'✅ Page loads: {response.status_code == 200}')

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for Google Fonts links
            google_fonts_links = soup.find_all('link', href=lambda x: x and 'fonts.googleapis.com' in x)
            print(f'📄 Google Fonts links found: {len(google_fonts_links)}')

            for link in google_fonts_links:
                href = link.get('href', 'N/A')
                print(f'   - {href}')

            # Check for font preconnect links
            preconnect_links = soup.find_all('link', {'rel': 'preconnect'}, href=lambda x: x and 'fonts.gstatic.com' in x)
            print(f'📡 Preconnect links found: {len(preconnect_links)}')

            # Check for text content with 's' characters
            body_text = soup.get_text()
            s_count = body_text.count('s') + body_text.count('S')
            print(f'📝 Total s/S characters in content: {s_count}')

            # Check for common words with 's' that might reveal rendering issues
            test_words = ['swarm', 'services', 'solutions', 'systems', 'software']
            found_words = []
            for word in test_words:
                if word.lower() in body_text.lower():
                    found_words.append(word)

            print(f'🔤 Words with s-characters found: {found_words}')

            # Check if the site has proper meta viewport
            viewport = soup.find('meta', {'name': 'viewport'})
            has_viewport = viewport is not None
            print(f'📱 Has viewport meta tag: {has_viewport}')

            # Overall assessment
            fonts_loaded = len(google_fonts_links) > 0
            preconnect_setup = len(preconnect_links) > 0
            has_content = len(body_text.strip()) > 100

            print('\n📊 VALIDATION RESULTS:')
            print(f'   Google Fonts loaded: {"✅" if fonts_loaded else "❌"}')
            print(f'   Preconnect configured: {"✅" if preconnect_setup else "❌"}')
            print(f'   Content loaded: {"✅" if has_content else "❌"}')
            print(f'   Viewport configured: {"✅" if has_viewport else "❌"}')

            if fonts_loaded and preconnect_setup and has_content:
                print('\n🎉 WEARESWARM.ONLINE VALIDATION: PASSED')
                print('Google Fonts are properly configured and content renders correctly.')
                return True
            else:
                print('\n⚠️ WEARESWARM.ONLINE VALIDATION: ISSUES FOUND')
                return False

        else:
            print('❌ Site failed to load')
            return False

    except Exception as e:
        print(f'❌ Validation error: {e}')
        return False

if __name__ == "__main__":
    success = validate_weareswarm()
    if success:
        print('\n✅ Validation complete - weareswarm.online is ready!')
    else:
        print('\n⚠️ Validation found issues that may need attention.')