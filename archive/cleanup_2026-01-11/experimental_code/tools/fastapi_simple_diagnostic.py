#!/usr/bin/env python3
"""
Simple FastAPI Performance Diagnostic
=====================================

Basic diagnostic for FastAPI performance issues.

Author: Agent-4 | Date: 2026-01-07
"""

import json
import time
import requests
from datetime import datetime

def test_fastapi_health():
    """Test FastAPI health endpoint response time."""

    urls_to_test = [
        "http://localhost:8000/health",
        "http://localhost:8001/health",
        "http://localhost:5000/health"
    ]

    results = {}

    print("🔍 Testing FastAPI health endpoints...")

    for url in urls_to_test:
        try:
            print(f"Testing {url}...")
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time

            results[url] = {
                "status": "success",
                "response_time": round(response_time, 3),
                "status_code": response.status_code,
                "threshold": 2.0,
                "within_threshold": response_time <= 2.0
            }

            print(f"  ✅ {url}: {response_time:.3f}s (status: {response.status_code})")

        except requests.exceptions.RequestException as e:
            results[url] = {
                "status": "error",
                "error": str(e),
                "response_time": None
            }
            print(f"  ❌ {url}: {e}")

    return results

def analyze_alerts():
    """Analyze recent alerts for patterns."""

    try:
        with open('alerts/alert_history.jsonl', 'r') as f:
            lines = f.readlines()

        fastapi_alerts = []
        other_alerts = []

        for line in lines[-20:]:  # Last 20 alerts
            try:
                alert = json.loads(line.strip())
                if "FastAPI" in alert.get("title", ""):
                    fastapi_alerts.append(alert)
                else:
                    other_alerts.append(alert)
            except:
                continue

        return {
            "fastapi_alerts_count": len(fastapi_alerts),
            "recent_fastapi_alerts": fastapi_alerts[-5:],  # Last 5 FastAPI alerts
            "other_alerts": other_alerts[-3:]  # Last 3 other alerts
        }

    except FileNotFoundError:
        return {"error": "alert_history.jsonl not found"}
    except Exception as e:
        return {"error": f"Error reading alerts: {e}"}

def main():
    """Run simple diagnostic."""

    print("🚀 FastAPI Simple Performance Diagnostic")
    print("=" * 50)

    # Test health endpoints
    health_results = test_fastapi_health()

    print("\n📊 Health Endpoint Results:")
    working_endpoints = []
    slow_endpoints = []

    for url, result in health_results.items():
        if result["status"] == "success":
            working_endpoints.append(url)
            if not result["within_threshold"]:
                slow_endpoints.append((url, result["response_time"]))

    print(f"Working endpoints: {len(working_endpoints)}")
    print(f"Slow endpoints (>2s): {len(slow_endpoints)}")

    if slow_endpoints:
        print("Slow endpoints:")
        for url, response_time in slow_endpoints:
            print(f"  • {url}: {response_time}s")

    # Analyze alerts
    print("\n📋 Recent Alert Analysis:")
    alert_analysis = analyze_alerts()

    if "error" in alert_analysis:
        print(f"Error reading alerts: {alert_analysis['error']}")
    else:
        fastapi_count = alert_analysis["fastapi_alerts_count"]
        print(f"FastAPI performance alerts (last 20): {fastapi_count}")

        if alert_analysis["recent_fastapi_alerts"]:
            print("Most recent FastAPI alerts:")
            for alert in alert_analysis["recent_fastapi_alerts"]:
                duration = alert.get("metadata", {}).get("duration", "N/A")
                print(f"  • {alert['timestamp'][:19]}: {duration}s")

    # Generate recommendations
    print("\n💡 Recommendations:")

    if not working_endpoints:
        print("❌ No FastAPI servers responding - check if servers are running")
    elif slow_endpoints:
        print("🐌 Performance issues detected:")
        print("  • Optimize database queries in health endpoint")
        print("  • Check for memory leaks")
        print("  • Review middleware and dependencies")
        print("  • Consider implementing caching")
    else:
        print("✅ All endpoints responding within acceptable time limits")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "health_test_results": health_results,
        "alert_analysis": alert_analysis,
        "working_endpoints": len(working_endpoints),
        "slow_endpoints": len(slow_endpoints)
    }

    with open('fastapi_simple_diagnostic.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Results saved to fastapi_simple_diagnostic.json")

if __name__ == "__main__":
    main()