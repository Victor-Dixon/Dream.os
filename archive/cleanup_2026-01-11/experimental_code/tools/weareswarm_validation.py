#!/usr/bin/env python3
"""
WearSwarm.online Validation Script
Validates Google Fonts loading and character rendering
"""

from .validation_utils import FontValidator, HTTPValidator

def validate_weareswarm():
    """Validate weareswarm.online Google Fonts and rendering"""

    print('🔍 Validating weareswarm.online Google Fonts rendering...')
    print('=' * 60)

    try:
        # Initialize validators
        http_validator = HTTPValidator("https://weareswarm.online")
        font_validator = FontValidator("https://weareswarm.online")

        # Check the main page
        page_result = http_validator.check_url('/')
        print(f'✅ Page loads: {page_result["success"]}')

        if page_result["success"]:
            # Validate font loading
            font_result = font_validator.validate_font_loading()
            print(f'📄 Google Fonts links found: {len(font_result.get("font_families_found", []))}')

            if "preconnect_configured" in font_result:
                print(f'📡 Preconnect configured: {"✅" if font_result["preconnect_configured"] else "❌"}')

            # Validate character rendering
            char_result = font_validator.validate_character_rendering()
            s_count = sum(char_result.get("character_counts", {}).values())
            print(f'📝 Total s/S characters in content: {s_count}')

            # Check for common words
            try:
                import requests
                response = requests.get('https://weareswarm.online', timeout=10)
                body_text = response.text.lower()
                test_words = ['swarm', 'services', 'solutions', 'systems', 'software']
                found_words = [word for word in test_words if word in body_text]
                print(f'🔤 Words with s-characters found: {found_words}')
            except Exception:
                print('🔤 Could not check word content')

            # Check viewport
            try:
                import requests
                from bs4 import BeautifulSoup
                response = requests.get('https://weareswarm.online', timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                viewport = soup.find('meta', {'name': 'viewport'})
                has_viewport = viewport is not None
                print(f'📱 Has viewport meta tag: {has_viewport}')
            except Exception:
                print('📱 Could not check viewport')

            # Overall assessment
            fonts_loaded = font_result.get("fonts_loaded", False)
            preconnect_setup = font_result.get("preconnect_configured", False)
            has_content = page_result.get("content_length", 0) > 100

            print('\n📊 VALIDATION RESULTS:')
            print(f'   Google Fonts loaded: {"✅" if fonts_loaded else "❌"}')
            print(f'   Preconnect configured: {"✅" if preconnect_setup else "❌"}')
            print(f'   Content loaded: {"✅" if has_content else "❌"}')
            print(f'   Characters render: {"✅" if char_result.get("characters_render", False) else "❌"}')

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