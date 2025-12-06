# XOXO Backend - Simple Setup Guide

Simple setup guide for running XOXO backend with **MariaDB and HeidiSQL only**.

## Quick Start

### 1. Install MariaDB
- Download from: https://mariadb.org/download/
- Install and set a root password
- Keep default port: 3306

### 2. Create Database in HeidiSQL
1. Open HeidiSQL
2. Connect to MariaDB (localhost:3306, user: root, your password)
3. Create database:
   ```sql
   CREATE DATABASE xoxo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 3. Setup Python Environment
```bash
cd XOXO_Python

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example env file
copy env.example .env

# Edit .env with your MariaDB password
notepad .env
```

**Update these in `.env`:**
```env
DB_PASSWORD=your_mariadb_root_password
JWT_SECRET=generate-a-strong-secret-here
```

**Optional (can leave empty):**
- `REDIS_URL=` (leave empty to disable Redis)
- `S3_ENDPOINT_URL=` (leave empty to disable photo uploads)

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start Server
```bash
python start.py
```

That's it! The server will start at http://localhost:8000

## What's Optional?

- **Redis**: Used for location caching. If not configured, nearby features still work but may be slower.
- **S3/MinIO**: Used for photo uploads. If not configured, photo upload endpoints will return an error.

## Troubleshooting

### Database Connection Error
- Check MariaDB service is running
- Verify database `xoxo_db` exists in HeidiSQL
- Check `.env` file has correct password

### Port Already in Use
- Change port in `start.py` or use: `uvicorn main:app --port 8001`

### Missing Dependencies
- Run: `pip install -r requirements.txt`

## API Documentation

Once server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

