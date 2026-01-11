import requests
import time

def check_fastapi_health():
    """Comprehensive FastAPI connectivity check"""
    print("🔍 FastAPI Connectivity Diagnosis")
    print("-" * 40)

    # Test basic connectivity
    try:
        print("Testing basic connectivity...")
        response = requests.get('http://localhost:8001/health', timeout=5)
        print(f"✅ HTTP {response.status_code} - Service responding")

        # Check response content
        data = response.json()
        print(f"Overall Status: {data.get('overall_status', 'unknown')}")
        print(f"Analytics Status: {data.get('analytics_status', 'unknown')}")
        print(f"FastAPI Status: {data.get('fastapi_status', 'unknown')}")

        if response.status_code == 200 and data.get('overall_status') == 'healthy':
            print("🎉 FastAPI service is fully operational!")
            return True
        else:
            print("⚠️ Service responding but may have issues")
            return True

    except requests.exceptions.Timeout:
        print("❌ Connection timeout - service not responding")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - service not running")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def check_key_endpoints():
    """Check key FastAPI endpoints"""
    print("\n🔗 Testing Key Endpoints")
    print("-" * 40)

    endpoints = [
        ('/docs', 'API Documentation'),
        ('/analytics/config', 'Analytics Config'),
        ('/performance/metrics', 'Performance Metrics'),
        ('/analytics/track', 'Analytics Tracking (POST)'),
    ]

    working_endpoints = 0

    for endpoint, description in endpoints:
        try:
            if endpoint == '/analytics/track':
                # POST request for analytics track
                response = requests.post(f'http://localhost:8001{endpoint}',
                                       json={'event_name': 'connectivity_test'},
                                       timeout=3)
            else:
                response = requests.get(f'http://localhost:8001{endpoint}', timeout=3)

            print(f"✅ {endpoint} - HTTP {response.status_code} ({description})")
            working_endpoints += 1

        except Exception as e:
            print(f"❌ {endpoint} - Failed ({description}): {str(e)[:50]}...")

    print(f"\n📊 Endpoint Status: {working_endpoints}/{len(endpoints)} operational")
    return working_endpoints == len(endpoints)

if __name__ == "__main__":
    health_ok = check_fastapi_health()
    endpoints_ok = check_key_endpoints()

    print("\n" + "=" * 50)
    if health_ok and endpoints_ok:
        print("🚀 FastAPI CONNECTIVITY: FULLY OPERATIONAL")
        print("✅ Ready for Agent-1 Revenue Engine validation")
    elif health_ok:
        print("⚠️ FastAPI CONNECTIVITY: PARTIALLY OPERATIONAL")
        print("⚠️ Health check OK, some endpoints may have issues")
    else:
        print("❌ FastAPI CONNECTIVITY: FAILED")
        print("❌ Service restoration required")
    print("=" * 50)