"""Unit tests for webhook endpoint."""
import pytest
import json
import hmac
import hashlib
from app import create_app
from database.mongo import get_db

@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/webhook_test_db'
    app.config['MONGO_DB_NAME'] = 'webhook_test_db'
    app.config['GITHUB_WEBHOOK_SECRET'] = 'test_secret'
    
    with app.test_client() as client:
        yield client
    
    # Cleanup: drop test database
    db = get_db()
    if db:
        db.client.drop_database('webhook_test_db')

def generate_signature(payload, secret):
    """Generate GitHub webhook signature."""
    hash_object = hmac.new(
        secret.encode('utf-8'),
        msg=payload.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    return 'sha256=' + hash_object.hexdigest()

def test_webhook_endpoint_push_event(client):
    """Test webhook endpoint with push event."""
    payload = {
        'ref': 'refs/heads/main',
        'repository': {
            'full_name': 'testuser/testrepo'
        },
        'sender': {
            'login': 'testuser'
        },
        'commits': [
            {'id': 'abc123', 'message': 'Test commit'}
        ]
    }
    
    payload_str = json.dumps(payload)
    signature = generate_signature(payload_str, 'test_secret')
    
    response = client.post(
        '/webhook',
        data=payload_str,
        content_type='application/json',
        headers={
            'X-Hub-Signature-256': signature,
            'X-GitHub-Event': 'push'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'event_id' in data


def test_webhook_endpoint_invalid_signature(client):
    """Test webhook endpoint with invalid signature."""
    payload = {
        'repository': {'full_name': 'testuser/testrepo'},
        'sender': {'login': 'testuser'}
    }
    
    response = client.post(
        '/webhook',
        json=payload,
        headers={
            'X-Hub-Signature-256': 'sha256=invalid',
            'X-GitHub-Event': 'push'
        }
    )
    
    assert response.status_code == 401


def test_webhook_endpoint_pull_request(client):
    """Test webhook endpoint with pull request event."""
    payload = {
        'action': 'opened',
        'repository': {
            'full_name': 'testuser/testrepo'
        },
        'sender': {
            'login': 'testuser'
        },
        'pull_request': {
            'number': 42,
            'title': 'Test PR',
            'state': 'open'
        }
    }
    
    payload_str = json.dumps(payload)
    signature = generate_signature(payload_str, 'test_secret')
    
    response = client.post(
        '/webhook',
        data=payload_str,
        content_type='application/json',
        headers={
            'X-Hub-Signature-256': signature,
            'X-GitHub-Event': 'pull_request'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'


def test_get_events_endpoint(client):
    """Test events API endpoint."""
    response = client.get('/api/events')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
