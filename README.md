# GitHub Webhook Receiver

A Flask application that receives GitHub webhook events, stores them in MongoDB, and displays them in a real-time UI.

## Features

- Receives GitHub webhook events (push, pull_request, etc.)
- Stores events in MongoDB
- Real-time UI that polls for new events every 15 seconds
- Dockerized deployment with Docker Compose

## Project Structure

```
webhook-repo/
├── app.py                  # Flask entry point
├── config.py               # App & Mongo config
├── requirements.txt        # Dependencies
├── database/               # MongoDB connection
├── models/                 # MongoDB schema
├── routes/                 # API endpoints
├── services/               # Business logic
├── utils/                  # Utility functions
├── ui/                     # Frontend files
├── tests/                  # Test files
└── docker/                 # Docker configuration
```

## Setup

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your configuration:
   ```
   MONGO_URI=mongodb://localhost:27017/webhook_db
   GITHUB_WEBHOOK_SECRET=your_secret_here
   ```
5. Run the application:
   ```bash
   python app.py
   ```

### Docker Deployment

```bash
cd docker
docker-compose up -d
```

## Configuration

Set the following environment variables in `.env`:

- `MONGO_URI`: MongoDB connection string
- `MONGO_DB_NAME`: Database name (default: webhook_db)
- `GITHUB_WEBHOOK_SECRET`: Secret for validating GitHub webhooks
- `SECRET_KEY`: Flask secret key
- `DEBUG`: Enable debug mode (default: False)

## GitHub Webhook Setup

1. Go to your GitHub repository settings
2. Navigate to Webhooks > Add webhook
3. Set Payload URL to: `http://your-domain.com/webhook`
4. Set Content type to: `application/json`
5. Set Secret to match your `GITHUB_WEBHOOK_SECRET`
6. Select events you want to receive
7. Save the webhook

## API Endpoints

- `GET /` - Serves the UI
- `POST /webhook` - Receives GitHub webhook events
- `GET /api/events` - Returns recent events (used by UI)

## License

MIT
