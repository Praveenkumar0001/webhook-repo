"""Manual database cleanup."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from config import Config

print("Connecting to MongoDB...")
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB_NAME]
collection = db['events']

print(f"Current events count: {collection.count_documents({})}")
print("\nDeleting all events...")

result = collection.delete_many({})
print(f"✅ Deleted {result.deleted_count} events")

print(f"\nNew count: {collection.count_documents({})}")
print("\n✅ Database cleaned! Now send test webhooks.")

client.close()
