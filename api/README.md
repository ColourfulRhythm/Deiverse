# DEIVERSE API Server

API server for handling repository connections and managing DEIVERSE integrations.

## Features

- Connect GitHub, GitLab, or Bitbucket repositories
- Store connection data in JSON file (for demo purposes)
- RESTful API endpoints
- CORS enabled for frontend integration

## Setup

### Node.js Version

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

The server will run on `http://localhost:3001`

### Python Version

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python server.py
```

The server will run on `http://localhost:3001`

## API Endpoints

### POST /api/connect-repo
Connect a repository to DEIVERSE.

**Request Body:**
```json
{
  "provider": "github",
  "repo_url": "https://github.com/username/repo",
  "branch": "main"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Repository connected successfully",
  "data": {
    "provider": "github",
    "repo_url": "https://github.com/username/repo",
    "branch": "main",
    "id": 1234567890,
    "connected_at": "2024-01-01T00:00:00",
    "status": "active"
  }
}
```

### GET /api/connections
Get all connected repositories.

**Response:**
```json
{
  "connections": [
    {
      "id": 1234567890,
      "provider": "github",
      "repo_url": "https://github.com/username/repo",
      "branch": "main",
      "connected_at": "2024-01-01T00:00:00",
      "status": "active"
    }
  ]
}
```

### GET /api/connections/:id
Get a specific connection by ID.

### GET /api/health
Health check endpoint.

## Production Notes

For production use:
- Replace JSON file storage with a proper database (PostgreSQL, MongoDB, etc.)
- Add authentication and authorization
- Implement rate limiting
- Add logging and monitoring
- Set up proper error handling

