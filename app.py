"""Flask entry point for GitHub webhook receiver."""
from flask import Flask, send_from_directory
from config import Config
from database.mongo import init_db
from routes.webhook import webhook_bp
from routes.events import events_bp
import os


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__, static_folder='ui', static_url_path='')
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(events_bp)
    
    @app.route('/')
    def index():
        """Serve the UI."""
        return send_from_directory('ui', 'index.html')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
