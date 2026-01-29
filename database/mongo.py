"""MongoDB connection handler."""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

db = None
client = None


def init_db(app):
    """Initialize MongoDB connection.
    
    Args:
        app: Flask application instance
    """
    global db, client
    
    try:
        mongo_uri = app.config['MONGO_URI']
        db_name = app.config['MONGO_DB_NAME']
        
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        
        db = client[db_name]
        app.logger.info(f"Successfully connected to MongoDB: {db_name}")
        
    except ConnectionFailure as e:
        app.logger.error(f"Failed to connect to MongoDB: {e}")
        raise


def get_db():
    """Get database instance.
    
    Returns:
        MongoDB database instance
    """
    return db


def close_db():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
