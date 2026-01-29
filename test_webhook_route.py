"""Test the /webhook route with sample GitHub events."""
import requests
import json
import hmac
import hashlib

# Server URL
BASE_URL = "http://localhost:5000"

# GitHub webhook secret (from .env)
WEBHOOK_SECRET = "your_github_webhook_secret_here"


def generate_signature(payload_body, secret):
    """Generate GitHub webhook signature."""
    if not secret:
        return None
    
    hash_object = hmac.new(
        secret.encode('utf-8'),
        msg=payload_body.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    return 'sha256=' + hash_object.hexdigest()


def test_push_event():
    """Test webhook with a push event."""
    print("Testing PUSH event...")
    print("-" * 50)
    
    payload = {
        "ref": "refs/heads/main",
        "repository": {
            "full_name": "testuser/testrepo"
        },
        "sender": {
            "login": "testuser"
        },
        "commits": [
            {
                "id": "abc123",
                "message": "Initial commit",
                "author": {"name": "Test User"}
            },
            {
                "id": "def456",
                "message": "Add feature",
                "author": {"name": "Test User"}
            }
        ]
    }
    
    payload_str = json.dumps(payload)
    signature = generate_signature(payload_str, WEBHOOK_SECRET)
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'push',
        'X-Hub-Signature-256': signature
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", data=payload_str, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Push event processed successfully!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


def test_pull_request_event():
    """Test webhook with a pull request event."""
    print("Testing PULL REQUEST event...")
    print("-" * 50)
    
    payload = {
        "action": "opened",
        "repository": {
            "full_name": "testuser/testrepo"
        },
        "sender": {
            "login": "contributor"
        },
        "pull_request": {
            "number": 42,
            "title": "Add new feature",
            "state": "open",
            "body": "This PR adds a new feature"
        }
    }
    
    payload_str = json.dumps(payload)
    signature = generate_signature(payload_str, WEBHOOK_SECRET)
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'pull_request',
        'X-Hub-Signature-256': signature
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", data=payload_str, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Pull request event processed successfully!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


def test_issues_event():
    """Test webhook with an issues event."""
    print("Testing ISSUES event...")
    print("-" * 50)
    
    payload = {
        "action": "opened",
        "repository": {
            "full_name": "testuser/testrepo"
        },
        "sender": {
            "login": "bugfinder"
        },
        "issue": {
            "number": 10,
            "title": "Found a bug",
            "state": "open",
            "body": "The app crashes when..."
        }
    }
    
    payload_str = json.dumps(payload)
    signature = generate_signature(payload_str, WEBHOOK_SECRET)
    
    headers = {
        'Content-Type': 'application/json',
        'X-GitHub-Event': 'issues',
        'X-Hub-Signature-256': signature
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", data=payload_str, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Issues event processed successfully!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


def verify_events_stored():
    """Verify events are stored in database."""
    print("Verifying stored events...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/events")
        events = response.json()
        print(f"Total events stored: {len(events)}")
        
        if events:
            print("\nRecent events:")
            for i, event in enumerate(events[:5], 1):
                print(f"{i}. {event['event_type']} - {event['action']} - {event['repository']} by {event['author']}")
        
        print("✅ Events retrieved successfully!\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")


if __name__ == '__main__':
    print("=" * 50)
    print("WEBHOOK ROUTE TEST SUITE")
    print("=" * 50)
    print(f"Server: {BASE_URL}")
    print("=" * 50)
    print()
    
    # Test different event types
    test_push_event()
    test_pull_request_event()
    test_issues_event()
    
    # Verify events are stored
    verify_events_stored()
    
    print("=" * 50)
    print("TEST COMPLETED")
    print("=" * 50)
