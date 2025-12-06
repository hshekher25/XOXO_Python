#!/usr/bin/env python3
"""
Simple server startup script for XOXO Backend
Just run: python start.py
"""
import os
import sys
import signal
import uvicorn
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_env_file():
    """Check if .env file exists, if not, create from example"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠ .env file not found. Creating from env.example...")
            import shutil
            shutil.copy(env_example, env_file)
            print("✓ Created .env file. Please update it with your MariaDB credentials!")
            print("  Edit .env and set:")
            print("  - DB_PASSWORD (your MariaDB root password)")
            print("  - JWT_SECRET (generate a strong secret)")
            print("\nPress Enter to continue anyway, or Ctrl+C to exit and configure...")
            try:
                input()
            except KeyboardInterrupt:
                print("\nExiting. Please configure .env file first.")
                sys.exit(1)
        else:
            print("⚠ .env file not found and env.example doesn't exist.")
            print("  Please create .env file with your configuration.")
            sys.exit(1)

def check_database_connection():
    """Check if database connection works"""
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        print("Checking database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✓ Database connection successful!")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("\nPlease check:")
        print("  1. MariaDB is running")
        print("  2. Database 'xoxo_db' exists (create it in HeidiSQL)")
        print("  3. .env file has correct DB credentials")
        print("\nTo create database in HeidiSQL:")
        print("  CREATE DATABASE xoxo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("XOXO Backend Server")
    print("=" * 60)
    print()
    
    # Check .env file
    check_env_file()
    
    # Check database
    if not check_database_connection():
        print("\n⚠ Starting server anyway, but database features may not work.")
        print("  Fix database connection and restart the server.\n")
    
    # Print configuration info
    from app.core.config import settings
    print(f"Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    print(f"Server: http://0.0.0.0:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print()
    print("Starting server...")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Start server with graceful shutdown handling
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

