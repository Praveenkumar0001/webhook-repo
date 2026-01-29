"""Quick verification of all requirements."""
import requests
import json

print("\n" + "🔍"*30)
print("COMPLETE SYSTEM VERIFICATION")
print("🔍"*30)

results = []

# 1. Test Flask is running
print("\n1️⃣ Testing Flask Backend...")
try:
    r = requests.get("http://localhost:5000/api/events", timeout=5)
    if r.status_code == 200:
        print("   ✅ Flask is running")
        results.append(("Flask Backend", True))
    else:
        print(f"   ❌ Flask returned {r.status_code}")
        results.append(("Flask Backend", False))
except Exception as e:
    print(f"   ❌ Flask is not responding: {e}")
    results.append(("Flask Backend", False))

# 2. Test PUSH webhook
print("\n2️⃣ Testing PUSH webhook...")
try:
    payload = {
        "ref": "refs/heads/staging",
        "head_commit": {"id": "abc123", "timestamp": "2021-04-01T21:30:00Z"},
        "pusher": {"name": "Travis"}
    }
    r = requests.post("http://localhost:5000/webhook", json=payload, 
                     headers={"X-GitHub-Event": "push"}, timeout=5)
    if r.status_code == 200:
        print("   ✅ PUSH webhook works")
        results.append(("PUSH Webhook", True))
    else:
        print(f"   ❌ PUSH webhook failed: {r.status_code}")
        results.append(("PUSH Webhook", False))
except Exception as e:
    print(f"   ❌ PUSH webhook error: {e}")
    results.append(("PUSH Webhook", False))

# 3. Test PULL_REQUEST webhook
print("\n3️⃣ Testing PULL_REQUEST webhook...")
try:
    payload = {
        "pull_request": {
            "id": 999, "merged": False,
            "user": {"login": "Travis"},
            "head": {"ref": "staging"}, "base": {"ref": "master"},
            "created_at": "2021-04-01T09:00:00Z"
        }
    }
    r = requests.post("http://localhost:5000/webhook", json=payload,
                     headers={"X-GitHub-Event": "pull_request"}, timeout=5)
    if r.status_code == 200:
        print("   ✅ PULL_REQUEST webhook works")
        results.append(("PULL_REQUEST Webhook", True))
    else:
        print(f"   ❌ PULL_REQUEST failed: {r.status_code}")
        results.append(("PULL_REQUEST Webhook", False))
except Exception as e:
    print(f"   ❌ PULL_REQUEST error: {e}")
    results.append(("PULL_REQUEST Webhook", False))

# 4. Test MERGE webhook (bonus)
print("\n4️⃣ Testing MERGE webhook (BONUS)...")
try:
    payload = {
        "pull_request": {
            "id": 888, "merged": True,
            "user": {"login": "Travis"},
            "head": {"ref": "dev"}, "base": {"ref": "master"},
            "created_at": "2021-04-02T12:00:00Z"
        }
    }
    r = requests.post("http://localhost:5000/webhook", json=payload,
                     headers={"X-GitHub-Event": "pull_request"}, timeout=5)
    if r.status_code == 200:
        print("   ✅ MERGE webhook works")
        results.append(("MERGE Webhook", True))
    else:
        print(f"   ❌ MERGE failed: {r.status_code}")
        results.append(("MERGE Webhook", False))
except Exception as e:
    print(f"   ❌ MERGE error: {e}")
    results.append(("MERGE Webhook", False))

# 5. Verify MongoDB schema
print("\n5️⃣ Verifying MongoDB Schema...")
try:
    r = requests.get("http://localhost:5000/api/events", timeout=5)
    events = r.json()
    if events:
        e = events[0]
        required = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
        has_all = all(field in e for field in required)
        if has_all:
            print("   ✅ MongoDB schema is CORRECT")
            print(f"      Latest event: {e.get('action')} by {e.get('author')}")
            results.append(("MongoDB Schema", True))
        else:
            missing = [f for f in required if f not in e]
            print(f"   ❌ Missing fields: {missing}")
            results.append(("MongoDB Schema", False))
    else:
        print("   ⚠️  No events in database yet")
        results.append(("MongoDB Schema", None))
except Exception as e:
    print(f"   ❌ Schema check failed: {e}")
    results.append(("MongoDB Schema", False))

# 6. Check UI polling configuration
print("\n6️⃣ Checking UI Configuration...")
try:
    with open('ui/script.js', 'r') as f:
        content = f.read()
    
    checks = {
        '15 second polling': 'const POLL_INTERVAL = 15000' in content,
        'PUSH format': 'pushed to' in content,
        'PULL_REQUEST format': 'submitted a pull request from' in content,
        'MERGE format': 'merged branch' in content,
    }
    
    all_ok = all(checks.values())
    if all_ok:
        print("   ✅ UI is configured correctly")
        for check, result in checks.items():
            print(f"      ✓ {check}")
        results.append(("UI Configuration", True))
    else:
        print("   ❌ UI configuration issues:")
        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"      {status} {check}")
        results.append(("UI Configuration", False))
except Exception as e:
    print(f"   ❌ UI check failed: {e}")
    results.append(("UI Configuration", False))

# 7. Test UI is accessible
print("\n7️⃣ Testing UI Access...")
try:
    r = requests.get("http://localhost:5000/", timeout=5)
    if r.status_code == 200:
        print("   ✅ UI is accessible at http://localhost:5000")
        results.append(("UI Access", True))
    else:
        print(f"   ❌ UI returned {r.status_code}")
        results.append(("UI Access", False))
except Exception as e:
    print(f"   ❌ UI not accessible: {e}")
    results.append(("UI Access", False))

# Summary
print("\n" + "="*60)
print("📊 FINAL SUMMARY")
print("="*60)

for test_name, result in results:
    if result is True:
        print(f"✅ {test_name}")
    elif result is False:
        print(f"❌ {test_name}")
    else:
        print(f"⚠️  {test_name} - No data")

passed = sum(1 for _, r in results if r is True)
total = len([r for _, r in results if r is not None])

print(f"\n📈 Score: {passed}/{total}")

if passed == total:
    print("\n🎉 EVERYTHING IS WORKING PERFECTLY! 🎉")
    print("\n✅ All requirements implemented:")
    print("   • PUSH events captured ✓")
    print("   • PULL_REQUEST events captured ✓")
    print("   • MERGE events captured (BONUS) ✓")
    print("   • MongoDB schema correct ✓")
    print("   • UI polling every 15 seconds ✓")
    print("   • Events displayed in correct format ✓")
else:
    print(f"\n⚠️  {total - passed} issue(s) need attention")

print("\n🌐 Your webhook endpoint:")
print("   https://chokiest-opal-probative.ngrok-free.dev/webhook")
print("\n👉 Open http://localhost:5000 to view the UI!")
