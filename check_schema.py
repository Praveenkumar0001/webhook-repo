import requests

r = requests.get('http://localhost:5000/api/events')
events = r.json()

print('Total events:', len(events))
print('\nLatest event schema:')
e = events[0]
print(f'  request_id: {e.get("request_id")}')
print(f'  author: {e.get("author")}')
print(f'  action: {e.get("action")}')
print(f'  from_branch: {e.get("from_branch")}')
print(f'  to_branch: {e.get("to_branch")}')
print(f'  timestamp: {e.get("timestamp")}')

# Check schema
required = ['request_id', 'author', 'action', 'from_branch', 'to_branch', 'timestamp']
missing = [f for f in required if f not in e]

if missing:
    print(f'\n❌ Missing fields: {missing}')
else:
    print('\n✅ All required fields present!')
