"""API endpoint for UI polling."""
from flask import Blueprint, jsonify
from models.event_model import EventModel

events_bp = Blueprint('events', __name__)


@events_bp.route('/api/events', methods=['GET'])
def get_events():
    """Get recent webhook events for UI display.
    
    Returns:
        JSON array of recent events
    """
    try:
        events = EventModel.get_recent_events(limit=50)
        return jsonify(events), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
