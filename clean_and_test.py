"""Clear old events and test with fresh data."""
from database.mongo import init_db, get_db
from app import create_app
import requests

print("🗑️  Clearing old events from MongoDB...")

# Initialize Flask app and database
app = create_app()
with app.app_context():
    db = get_db()
    collection = db['events']
    
    # Delete all old events
    result = collection.delete_many({})
    print(f"   ✅ Deleted {result.deleted_count} old events")

print("\n📝 Creating fresh test events...")

# Test PUSH event
print("\n1. Testing PUSH event...")
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
r = requests.post("http://localhost:5000/webhook", json=payload, 
                 headers={"X-GitHub-Event": "push"})
print(f"   Status: {r.status_code}")

# Test PULL_REQUEST event
print("\n2. Testing PULL_REQUEST event...")
payload = {
    "pull_request": {
        "id": 12345,
        "merged": False,
        "user": {"login": "Travis"},
        "head": {"ref": "staging"},
        "base": {"ref": "master"},
        "created_at": "2021-04-01T09:00:00Z"
    }
}
r = requests.post("http://localhost:5000/webhook", json=payload,
                 headers={"X-GitHub-Event": "pull_request"})
print(f"   Status: {r.status_code}")

# Test MERGE event
print("\n3. Testing MERGE event...")
payload = {
    "pull_request": {
        "id": 67890,
        "merged": True,
        "user": {"login": "Travis"},
        "head": {"ref": "dev"},
        "base": {"ref": "master"},
        "created_at": "2021-04-02T12:00:00Z"
    }
}
r = requests.post("http://localhost:5000/webhook", json=payload,
                 headers={"X-GitHub-Event": "pull_request"})
print(f"   Status: {r.status_code}")

# Verify schema
print("\n✅ Verifying MongoDB Schema...")
r = requests.get("http://localhost:5000/api/events")
events = r.json()

print(f"\nTotal events: {len(events)}")

for i, e in enumerate(events, 1):
    print(f"\n{i}. {e.get('action')} event:")
    print(f"   request_id: {e.get('request_id')}")
    print(f"   author: {e.get('author')}")
    print(f"   action: {e.get('action')}")
    print(f"   from_branch: {e.get('from_branch')}")
    print(f"   to_branch: {e.get('to_branch')}")
    print(f"   timestamp: {e.get('timestamp')}")
    
    # Check schema
    required = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
    has_all = all(field in e for field in required)
    
    if has_all:
        print(f"   ✅ Schema: CORRECT")
    else:
        missing = [f for f in required if f not in e]
        print(f"   ❌ Schema: Missing {missing}")

print("\n" + "="*60)
print("✅ Database cleaned and fresh events created!")
print("="*60)
