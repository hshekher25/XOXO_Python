#!/usr/bin/env python3
"""
Script to create all database tables automatically.
Run this after setting up your MariaDB database.
"""
from app.core.database import Base, engine
from app.models import (
    User,
    Profile,
    Swipe,
    Match,
    ChatMessage,
    ChatRoom,
    ChatRoomMessage,
    NearbyChat,
    NearbyChatMessage,
)

def create_tables():
    """Create all tables defined in models."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
    print("\nCreated tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")

if __name__ == "__main__":
    try:
        create_tables()
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        print("\nMake sure:")
        print("  1. MariaDB is running")
        print("  2. Database 'xoxo_db' exists")
        print("  3. Credentials in .env or config.py are correct")
        exit(1)

