#!/usr/bin/env python3
"""
Check freerideinvestor.com HTTP Status
======================================
Quick diagnostic to check current site status
"""

import urllib.request
import urllib.error
import sys

def check_site():
    url = "https://freerideinvestor.com"
    print(f"🔍 Checking {url}...")
    print("=" * 60)
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            content = response.read()
            content_length = len(content)
            content_preview = content[:500].decode('utf-8', errors='ignore')
            
            print(f"✅ Status Code: {status}")
            print(f"📊 Content Length: {content_length} bytes")
            print(f"\n📄 Content Preview (first 500 chars):")
            print("-" * 60)
            print(content_preview)
            print("-" * 60)
            
            if status == 200:
                print("\n✅ Site is accessible!")
            else:
                print(f"\n⚠️  Site returned status {status}")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        try:
            error_content = e.read().decode('utf-8', errors='ignore')
            print(f"📄 Error Response ({len(error_content)} bytes):")
            print("-" * 60)
            print(error_content[:1000])
            print("-" * 60)
        except:
            pass
        return False
        
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = check_site()
    sys.exit(0 if success else 1)



