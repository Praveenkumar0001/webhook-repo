"""UTC time formatting utilities."""
from datetime import datetime


def format_utc_time(dt=None):
    """Format datetime to UTC ISO format.
    
    Args:
        dt: datetime object (default: current UTC time)
        
    Returns:
        ISO formatted UTC timestamp
    """
    if dt is None:
        dt = datetime.utcnow()
    
    return dt.isoformat() + 'Z'


def parse_utc_time(time_string):
    """Parse ISO formatted UTC timestamp.
    
    Args:
        time_string: ISO formatted timestamp string
        
    Returns:
        datetime object
    """
    # Remove 'Z' suffix if present
    if time_string.endswith('Z'):
        time_string = time_string[:-1]
    
    return datetime.fromisoformat(time_string)


def get_current_utc():
    """Get current UTC datetime.
    
    Returns:
        Current UTC datetime object
    """
    return datetime.utcnow()
