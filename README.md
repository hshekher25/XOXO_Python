# XOXO Python Backend

FastAPI backend for the XOXO dating app with retro chat rooms and nearby features.

## Features

- **Auth Module**: JWT-based authentication with refresh tokens
- **Profiles Module**: User profile management with photo uploads
- **Swipe/Match Module**: Swipe functionality and match creation
- **Chat Module**: One-on-one messaging between matches
- **Chat Rooms Module**: Public topic-based chat rooms (retro style)
- **Nearby Users Module**: Location-based user discovery and temporary chat rooms
- **WebSocket Support**: Real-time messaging via WebSockets

## Setup

### Prerequisites

- Python 3.9+
- MariaDB (or MySQL)
- Redis
- MinIO (S3-compatible storage)

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your configuration
```

**IMPORTANT for Production/VPS:**
- Change all default passwords
- Generate strong JWT_SECRET: `openssl rand -hex 32`
- Restrict file permissions: `chmod 600 .env`
- Never commit `.env` to version control

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

See `env.example` for all required environment variables.

The application reads configuration from:
1. Environment variables (highest priority)
2. `.env` file in the project root
3. Default values in `app/core/config.py` (lowest priority)

**Key Configuration:**
- **Database**: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- **JWT**: `JWT_SECRET` (MUST be changed in production!)
- **Redis**: `REDIS_URL`
- **S3/MinIO**: `S3_ENDPOINT_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET_NAME`

For VPS deployment, see [VPS_DEPLOYMENT.md](../docs/VPS_DEPLOYMENT.md).

## Project Structure

```
XOXO_Python/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/    # API endpoints
│   │       └── api.py        # Router configuration
│   ├── core/                 # Core configuration
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic services
│   └── websocket/            # WebSocket handlers
├── alembic/                  # Database migrations
├── main.py                   # Application entry point
└── requirements.txt          # Python dependencies
```
