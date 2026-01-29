"""MongoDB schema for GitHub webhook events."""
from datetime import datetime
from database.mongo import get_db


class EventModel:
    """Model for GitHub webhook events."""
    
    COLLECTION_NAME = 'events'
    
    @staticmethod
    def create_event(event_data):
        """Create a new event in the database.
        
        Args:
            event_data: Dictionary containing event information
            
        Returns:
            Inserted document ID
        """
        db = get_db()
        collection = db[EventModel.COLLECTION_NAME]
        
        # Convert timestamp string to datetime for proper sorting
        timestamp_str = event_data.get('timestamp')
        timestamp_dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Store exactly as per requirements schema
        document = {
            'request_id': event_data.get('request_id'),
            'author': event_data.get('author'),
            'action': event_data.get('action'),
            'from_branch': event_data.get('from_branch'),
            'to_branch': event_data.get('to_branch'),
            'timestamp': timestamp_str,  # Keep original string format for display
            'timestamp_dt': timestamp_dt  # Add datetime for sorting
        }
        
        result = collection.insert_one(document)
        return result.inserted_id
    
    @staticmethod
    def get_recent_events(limit=50):
        """Get recent events from the database.
        
        Args:
            limit: Maximum number of events to retrieve
            
        Returns:
            List of event documents
        """
        db = get_db()
        collection = db[EventModel.COLLECTION_NAME]
        
        # Sort by timestamp_dt (datetime) instead of timestamp (string) for proper chronological order
        events = collection.find().sort('timestamp_dt', -1).limit(limit)
        
        # Convert ObjectId to string for JSON serialization
        result = []
        for event in events:
            event['_id'] = str(event['_id'])
            # Remove timestamp_dt from response (only used for sorting)
            if 'timestamp_dt' in event:
                del event['timestamp_dt']
            result.append(event)
        
        return result
    
    @staticmethod
    def get_event_by_id(event_id):
        """Get a specific event by ID.
        
        Args:
            event_id: Event document ID
            
        Returns:
            Event document or None
        """
        from bson.objectid import ObjectId
        
        db = get_db()
        collection = db[EventModel.COLLECTION_NAME]
        
        event = collection.find_one({'_id': ObjectId(event_id)})
        if event:
            event['_id'] = str(event['_id'])
        
        return event
    
    @staticmethod
    def delete_old_events(days=30):
        """Delete events older than specified days.
        
        Args:
            days: Number of days to retain
            
        Returns:
            Number of deleted documents
        """
        from datetime import timedelta
        
        db = get_db()
        collection = db[EventModel.COLLECTION_NAME]
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = collection.delete_many({'timestamp': {'$lt': cutoff_date}})
        
        return result.deleted_count
