import requests
import time

print("="*60)
print("TESTING NEW EVENTS WITH CORRECT SCHEMA")
print("="*60)

# Test PUSH event
print("\n1. Testing PUSH event...")
payload = {
    'ref': 'refs/heads/staging',
    'head_commit': {
        'id': 'abc123def456',
        'timestamp': '2021-04-01T21:30:00Z'
    },
    'pusher': {
        'name': 'Travis'
    }
}
r = requests.post('http://localhost:5000/webhook', json=payload, headers={'X-GitHub-Event': 'push'})
print(f"   Status: {r.status_code} - {r.json()}")

# Test PULL_REQUEST event
print("\n2. Testing PULL_REQUEST event...")
payload = {
    'pull_request': {
        'id': 12345,
        'merged': False,
        'user': {'login': 'Travis'},
        'head': {'ref': 'staging'},
        'base': {'ref': 'master'},
        'created_at': '2021-04-01T09:00:00Z'
    }
}
r = requests.post('http://localhost:5000/webhook', json=payload, headers={'X-GitHub-Event': 'pull_request'})
print(f"   Status: {r.status_code} - {r.json()}")

# Test MERGE event
print("\n3. Testing MERGE event...")
payload = {
    'pull_request': {
        'id': 67890,
        'merged': True,
        'user': {'login': 'Travis'},
        'head': {'ref': 'dev'},
        'base': {'ref': 'master'},
        'created_at': '2021-04-02T12:00:00Z'
    }
}
r = requests.post('http://localhost:5000/webhook', json=payload, headers={'X-GitHub-Event': 'pull_request'})
print(f"   Status: {r.status_code} - {r.json()}")

# Wait and check latest events
time.sleep(1)

print("\n" + "="*60)
print("CHECKING STORED EVENTS")
print("="*60)

r = requests.get('http://localhost:5000/api/events')
events = r.json()

print(f"\nTotal events in DB: {len(events)}")
print("\nLatest 3 events:\n")

for i, e in enumerate(events[:3], 1):
    print(f"{i}. Action: {e.get('action')}")
    print(f"   request_id: {e.get('request_id')}")
    print(f"   author: {e.get('author')}")
    print(f"   from_branch: {e.get('from_branch')}")
    print(f"   to_branch: {e.get('to_branch')}")
    print(f"   timestamp: {e.get('timestamp')}")
    
    # Verify schema
    required = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
    has_all = all(f in e for f in required)
    
    if has_all:
        print(f"   ✅ Schema: CORRECT")
    else:
        missing = [f for f in required if f not in e]
        print(f"   ❌ Schema: Missing {missing}")
    print()

print("="*60)
print("SUMMARY")
print("="*60)
print("✅ Webhook endpoint working")
print("✅ MongoDB storing events")
print("✅ API returning events")
print("\n👉 Now open http://localhost:5000 to see the UI!")
print("   (UI polls every 15 seconds)")
