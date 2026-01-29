"""Application and MongoDB configuration."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for Flask app."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False  # Disabled to prevent reloader issues
    
    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/webhook_db')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'webhook_db')
    
    # GitHub webhook settings
    GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET', '')
