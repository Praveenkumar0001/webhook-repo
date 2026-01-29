"""Test MongoDB connection."""
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config

def test_connection():
    """Test MongoDB connection with current configuration."""
    print("Testing MongoDB connection...")
    print(f"MongoDB URI: {Config.MONGO_URI[:20]}...") # Show only first 20 chars for security
    print(f"Database Name: {Config.MONGO_DB_NAME}")
    print("-" * 50)
    
    try:
        # Create MongoDB client with timeout
        client = MongoClient(
            Config.MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
        
        # Test the connection by pinging the server
        print("Attempting to connect...")
        client.admin.command('ping')
        
        print("✅ SUCCESS: Connected to MongoDB!")
        
        # Get database
        db = client[Config.MONGO_DB_NAME]
        
        # List collections
        collections = db.list_collection_names()
        print(f"\nDatabase: {Config.MONGO_DB_NAME}")
        print(f"Collections: {collections if collections else 'No collections yet'}")
        
        # Get server info
        server_info = client.server_info()
        print(f"\nMongoDB Version: {server_info.get('version', 'Unknown')}")
        
        # Close connection
        client.close()
        print("\n✅ Connection test completed successfully!")
        return True
        
    except ServerSelectionTimeoutError as e:
        print("❌ ERROR: Could not connect to MongoDB server")
        print(f"Reason: Connection timeout - server not reachable")
        print(f"Details: {e}")
        return False
        
    except ConnectionFailure as e:
        print("❌ ERROR: MongoDB connection failed")
        print(f"Details: {e}")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: Unexpected error occurred")
        print(f"Type: {type(e).__name__}")
        print(f"Details: {e}")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
