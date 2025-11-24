"""
Script to create sample chat rooms in the database.
Run this script to populate the database with some default chat rooms.
"""
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.chat_room import ChatRoom
from app.models.user import User

# Database connection
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    f"?charset=utf8mb4"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample chat rooms to create
SAMPLE_ROOMS = [
    {
        "name": "General",
        "topic": "General Discussion",
        "description": "A place for general conversations and introductions"
    },
    {
        "name": "Tech Talk",
        "topic": "Technology",
        "description": "Discuss the latest tech trends, programming, and gadgets"
    },
    {
        "name": "Music",
        "topic": "Music & Entertainment",
        "description": "Share your favorite songs, artists, and music recommendations"
    },
    {
        "name": "Gaming",
        "topic": "Gaming",
        "description": "Talk about games, strategies, and find gaming buddies"
    },
    {
        "name": "Movies",
        "topic": "Movies & TV Shows",
        "description": "Discuss movies, TV series, and share recommendations"
    },
    {
        "name": "Fitness",
        "topic": "Health & Fitness",
        "description": "Share workout tips, nutrition advice, and fitness goals"
    },
    {
        "name": "Food",
        "topic": "Food & Cooking",
        "description": "Share recipes, restaurant reviews, and food adventures"
    },
    {
        "name": "Travel",
        "topic": "Travel & Adventure",
        "description": "Share travel experiences, tips, and destination recommendations"
    }
]


def create_chat_rooms():
    """Create sample chat rooms in the database."""
    db = SessionLocal()
    
    try:
        # Get the first user as the creator (or create a system user)
        first_user = db.query(User).first()
        
        if not first_user:
            print("ERROR: No users found in database. Please create a user first.")
            print("You can register a user through the app or create one manually.")
            return
        
        print(f"Using user '{first_user.email}' as room creator")
        print(f"\nCreating {len(SAMPLE_ROOMS)} chat rooms...\n")
        
        created_count = 0
        skipped_count = 0
        
        for room_data in SAMPLE_ROOMS:
            # Check if room already exists
            existing_room = db.query(ChatRoom).filter(ChatRoom.name == room_data["name"]).first()
            
            if existing_room:
                print(f"[SKIP] '{room_data['name']}' - already exists")
                skipped_count += 1
                continue
            
            # Create new room
            new_room = ChatRoom(
                name=room_data["name"],
                topic=room_data["topic"],
                description=room_data["description"],
                created_by=first_user.id
            )
            
            db.add(new_room)
            db.commit()
            db.refresh(new_room)
            
            print(f"[OK] Created '{room_data['name']}' (ID: {new_room.id})")
            created_count += 1
        
        print(f"\n{'='*50}")
        print(f"Summary:")
        print(f"  Created: {created_count} rooms")
        print(f"  Skipped: {skipped_count} rooms (already exist)")
        print(f"{'='*50}")
        
    except Exception as e:
        db.rollback()
        print(f"ERROR: Failed to create chat rooms: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("="*50)
    print("Chat Room Creation Script")
    print("="*50)
    print()
    
    create_chat_rooms()
    
    print("\nDone! You can now see these rooms in the app.")

