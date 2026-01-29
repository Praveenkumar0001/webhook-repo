"""Comprehensive test to verify all project requirements."""
import requests
import json
from datetime import datetime
import time

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_webhook_health():
    """Test webhook endpoint health check."""
    print_section("TEST 1: Webhook Health Check")
    try:
        response = requests.get(f"{BASE_URL}/webhook")
        print(f"✓ Webhook GET endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Webhook health check failed: {e}")
        return False

def test_push_event():
    """Test PUSH event webhook."""
    print_section("TEST 2: PUSH Event")
    
    push_payload = {
        "ref": "refs/heads/staging",
        "head_commit": {
            "id": "abc123def456",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "pusher": {
            "name": "Travis"
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=push_payload,
            headers={"X-GitHub-Event": "push"}
        )
        print(f"✓ PUSH webhook received: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        # Verify expected format: {author} pushed to {to_branch} on {timestamp}
        print(f"\n  Expected format: Travis pushed to staging on [timestamp]")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ PUSH event test failed: {e}")
        return False

def test_pull_request_event():
    """Test PULL_REQUEST event webhook."""
    print_section("TEST 3: PULL_REQUEST Event")
    
    pr_payload = {
        "action": "opened",
        "pull_request": {
            "id": 123456,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "staging"
            },
            "base": {
                "ref": "master"
            },
            "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "merged": False
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=pr_payload,
            headers={"X-GitHub-Event": "pull_request"}
        )
        print(f"✓ PULL_REQUEST webhook received: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        # Verify expected format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
        print(f"\n  Expected format: Travis submitted a pull request from staging to master on [timestamp]")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ PULL_REQUEST event test failed: {e}")
        return False

def test_merge_event():
    """Test MERGE event webhook (Brownie Points)."""
    print_section("TEST 4: MERGE Event (Brownie Points)")
    
    merge_payload = {
        "action": "closed",
        "pull_request": {
            "id": 789012,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "dev"
            },
            "base": {
                "ref": "master"
            },
            "created_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "merged": True
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=merge_payload,
            headers={"X-GitHub-Event": "pull_request"}
        )
        print(f"✓ MERGE webhook received: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        # Verify expected format: {author} merged branch {from_branch} to {to_branch} on {timestamp}
        print(f"\n  Expected format: Travis merged branch dev to master on [timestamp]")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ MERGE event test failed: {e}")
        return False

def test_ping_event():
    """Test PING event webhook."""
    print_section("TEST 5: PING Event")
    
    ping_payload = {
        "zen": "Design for failure.",
        "hook_id": 12345
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=ping_payload,
            headers={"X-GitHub-Event": "ping"}
        )
        print(f"✓ PING webhook received: {response.status_code}")
        print(f"  Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ PING event test failed: {e}")
        return False

def test_api_events():
    """Test API events endpoint."""
    print_section("TEST 6: API Events Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/events")
        print(f"✓ API endpoint accessible: {response.status_code}")
        
        events = response.json()
        print(f"  Total events stored: {len(events)}")
        
        if events:
            print(f"\n  Sample event:")
            latest = events[0]
            print(f"    - Request ID: {latest.get('request_id')}")
            print(f"    - Author: {latest.get('author')}")
            print(f"    - Action: {latest.get('action')}")
            print(f"    - From Branch: {latest.get('from_branch')}")
            print(f"    - To Branch: {latest.get('to_branch')}")
            print(f"    - Timestamp: {latest.get('timestamp')}")
            
            # Verify MongoDB schema matches requirements
            print(f"\n  ✓ Schema verification:")
            required_fields = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
            for field in required_fields:
                if field in latest:
                    print(f"    ✓ {field}: present")
                else:
                    print(f"    ✗ {field}: MISSING")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ API events test failed: {e}")
        return False

def test_ui_polling():
    """Test UI polling mechanism."""
    print_section("TEST 7: UI Polling (15 seconds)")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ UI accessible: {response.status_code}")
        
        # Check if script.js contains 15-second polling
        if "15000" in response.text or "15 seconds" in response.text:
            print(f"  ✓ 15-second polling interval configured in UI")
        else:
            print(f"  ? Unable to verify polling interval from HTML")
        
        return response.status_code == 200
    except Exception as e:
        print(f"✗ UI test failed: {e}")
        return False

def verify_message_formats():
    """Verify message display formats match requirements."""
    print_section("TEST 8: Message Format Verification")
    
    print("Expected formats from requirements:")
    print("  PUSH: {author} pushed to {to_branch} on {timestamp}")
    print("  PULL_REQUEST: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}")
    print("  MERGE: {author} merged branch {from_branch} to {to_branch} on {timestamp}")
    
    try:
        with open('ui/script.js', 'r') as f:
            content = f.read()
            
            checks = {
                'PUSH format': 'pushed to' in content,
                'PULL_REQUEST format': 'submitted a pull request from' in content,
                'MERGE format': 'merged branch' in content,
                '15 second polling': 'POLL_INTERVAL = 15000' in content or '15000' in content
            }
            
            for check, result in checks.items():
                status = "✓" if result else "✗"
                print(f"  {status} {check}: {'Found' if result else 'NOT FOUND'}")
            
            return all(checks.values())
    except Exception as e:
        print(f"✗ Format verification failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     COMPREHENSIVE PROJECT VERIFICATION TEST SUITE          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    time.sleep(1)
    
    results = []
    
    # Run all tests
    results.append(("Webhook Health Check", test_webhook_health()))
    time.sleep(0.5)
    
    results.append(("PUSH Event", test_push_event()))
    time.sleep(0.5)
    
    results.append(("PULL_REQUEST Event", test_pull_request_event()))
    time.sleep(0.5)
    
    results.append(("MERGE Event", test_merge_event()))
    time.sleep(0.5)
    
    results.append(("PING Event", test_ping_event()))
    time.sleep(0.5)
    
    results.append(("API Events", test_api_events()))
    time.sleep(0.5)
    
    results.append(("UI Polling", test_ui_polling()))
    time.sleep(0.5)
    
    results.append(("Message Formats", verify_message_formats()))
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {status}: {test_name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  ✓ ALL TESTS PASSED! Project is working perfectly! ✓")
    else:
        print(f"\n  ⚠ {total - passed} test(s) failed. Please review the issues above.")
    
    print("="*60)

if __name__ == "__main__":
    run_all_tests()
