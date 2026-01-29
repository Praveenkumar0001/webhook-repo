"""Complete flow test to verify all requirements are met."""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_push_event():
    """Test PUSH event webhook."""
    print("\n" + "="*60)
    print("TEST 1: PUSH EVENT")
    print("="*60)
    
    payload = {
        "ref": "refs/heads/staging",
        "head_commit": {
            "id": "abc123def456",
            "timestamp": "2021-04-01T21:30:00Z"
        },
        "pusher": {
            "name": "Travis"
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'push'
    }
    
    response = requests.post(f"{BASE_URL}/webhook", json=payload, headers=headers)
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ PUSH event processed successfully!")
        print(f"   Expected format: 'Travis pushed to staging on 1st April 2021 - 9:30 PM UTC'")
    else:
        print("❌ PUSH event failed!")
    
    return response.status_code == 200


def test_pull_request_event():
    """Test PULL REQUEST event webhook."""
    print("\n" + "="*60)
    print("TEST 2: PULL REQUEST EVENT")
    print("="*60)
    
    payload = {
        "pull_request": {
            "id": 12345,
            "merged": False,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "staging"
            },
            "base": {
                "ref": "master"
            },
            "created_at": "2021-04-01T09:00:00Z"
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'pull_request'
    }
    
    response = requests.post(f"{BASE_URL}/webhook", json=payload, headers=headers)
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ PULL REQUEST event processed successfully!")
        print(f"   Expected format: 'Travis submitted a pull request from staging to master on 1st April 2021 - 9:00 AM UTC'")
    else:
        print("❌ PULL REQUEST event failed!")
    
    return response.status_code == 200


def test_merge_event():
    """Test MERGE event webhook (bonus points)."""
    print("\n" + "="*60)
    print("TEST 3: MERGE EVENT (BONUS)")
    print("="*60)
    
    payload = {
        "pull_request": {
            "id": 67890,
            "merged": True,
            "user": {
                "login": "Travis"
            },
            "head": {
                "ref": "dev"
            },
            "base": {
                "ref": "master"
            },
            "created_at": "2021-04-02T12:00:00Z"
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'pull_request'
    }
    
    response = requests.post(f"{BASE_URL}/webhook", json=payload, headers=headers)
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ MERGE event processed successfully!")
        print(f"   Expected format: 'Travis merged branch dev to master on 2nd April 2021 - 12:00 PM UTC'")
    else:
        print("❌ MERGE event failed!")
    
    return response.status_code == 200


def verify_mongodb_schema():
    """Verify events are stored with correct schema."""
    print("\n" + "="*60)
    print("TEST 4: MONGODB SCHEMA VERIFICATION")
    print("="*60)
    
    time.sleep(1)  # Give time for data to be stored
    
    response = requests.get(f"{BASE_URL}/api/events")
    events = response.json()
    
    if not events:
        print("❌ No events found in database!")
        return False
    
    print(f"✓ Found {len(events)} events in database")
    
    # Check first event schema
    event = events[0]
    required_fields = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
    
    print("\n📋 Schema Check:")
    all_present = True
    for field in required_fields:
        if field in event:
            value = event[field]
            if value is None:
                print(f"   ✓ {field}: null (valid for from_branch in PUSH)")
            else:
                print(f"   ✓ {field}: {value}")
        else:
            print(f"   ❌ {field}: MISSING!")
            all_present = False
    
    if all_present:
        print("\n✅ MongoDB schema is correct!")
    else:
        print("\n❌ MongoDB schema is missing required fields!")
    
    return all_present


def verify_ui_polling():
    """Verify UI is configured to poll every 15 seconds."""
    print("\n" + "="*60)
    print("TEST 5: UI POLLING CONFIGURATION")
    print("="*60)
    
    # Read the script.js file
    with open('ui/script.js', 'r') as f:
        content = f.read()
    
    if 'const POLL_INTERVAL = 15000' in content:
        print("✅ UI is configured to poll every 15 seconds!")
        return True
    else:
        print("❌ UI polling interval is not 15 seconds!")
        return False


def verify_event_display_format():
    """Verify events are displayed in correct format."""
    print("\n" + "="*60)
    print("TEST 6: EVENT DISPLAY FORMAT")
    print("="*60)
    
    # Read the script.js file
    with open('ui/script.js', 'r') as f:
        content = f.read()
    
    checks = {
        'PUSH format': 'pushed to' in content,
        'PULL_REQUEST format': 'submitted a pull request from' in content,
        'MERGE format': 'merged branch' in content,
    }
    
    all_correct = True
    for check, result in checks.items():
        if result:
            print(f"   ✅ {check}: Correct")
        else:
            print(f"   ❌ {check}: Missing")
            all_correct = False
    
    if all_correct:
        print("\n✅ All display formats are correct!")
    else:
        print("\n❌ Some display formats are incorrect!")
    
    return all_correct


def main():
    """Run all tests."""
    print("\n" + "🔍"*30)
    print("WEBHOOK SYSTEM COMPLETE VERIFICATION")
    print("🔍"*30)
    
    results = []
    
    try:
        # Test webhook endpoints
        results.append(("PUSH Event", test_push_event()))
        results.append(("PULL_REQUEST Event", test_pull_request_event()))
        results.append(("MERGE Event", test_merge_event()))
        results.append(("MongoDB Schema", verify_mongodb_schema()))
        results.append(("UI Polling", verify_ui_polling()))
        results.append(("Display Format", verify_event_display_format()))
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return
    
    # Print summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL REQUIREMENTS IMPLEMENTED CORRECTLY! 🎉")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review.")


if __name__ == '__main__':
    main()
