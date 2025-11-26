"""
Script to create sample chat rooms via the API.
This uses HTTP requests to create rooms, so it works with any backend setup.
"""
import requests
import json
import sys

# Backend API URL
BASE_URL = "http://localhost:8000/api/v1"

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


def create_chat_rooms(email: str, password: str):
    """Create chat rooms via API."""
    
    # Step 1: Login to get access token
    print("Logging in...")
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "username": email,  # FastAPI OAuth2 uses 'username' field
        "password": password
    }
    
    try:
        login_response = requests.post(login_url, data=login_data)
        if login_response.status_code != 200:
            print(f"ERROR: Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("ERROR: No access token received")
            return
        
        print("Login successful!\n")
        
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to backend at {BASE_URL}")
        print("Make sure the backend server is running.")
        return
    except Exception as e:
        print(f"ERROR: Login failed: {e}")
        return
    
    # Step 2: Create chat rooms
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    create_url = f"{BASE_URL}/chat-rooms"
    
    print(f"Creating {len(SAMPLE_ROOMS)} chat rooms...\n")
    
    created_count = 0
    skipped_count = 0
    error_count = 0
    
    for room_data in SAMPLE_ROOMS:
        try:
            response = requests.post(
                create_url,
                headers=headers,
                json=room_data
            )
            
            if response.status_code == 201:
                room = response.json()
                print(f"[OK] Created '{room_data['name']}' (ID: {room['id']})")
                created_count += 1
            elif response.status_code == 400:
                error_data = response.json()
                if "already exists" in error_data.get("detail", ""):
                    print(f"[SKIP] '{room_data['name']}' - already exists")
                    skipped_count += 1
                else:
                    print(f"[ERROR] '{room_data['name']}': {error_data.get('detail', 'Unknown error')}")
                    error_count += 1
            else:
                print(f"[ERROR] '{room_data['name']}': HTTP {response.status_code}")
                print(f"  Response: {response.text}")
                error_count += 1
                
        except Exception as e:
            print(f"[ERROR] '{room_data['name']}': {e}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Created: {created_count} rooms")
    print(f"  Skipped: {skipped_count} rooms (already exist)")
    print(f"  Errors: {error_count} rooms")
    print(f"{'='*50}")


if __name__ == "__main__":
    print("="*50)
    print("Chat Room Creation Script (via API)")
    print("="*50)
    print()
    
    # Get credentials from command line or use defaults
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        print("Usage: python create_chat_rooms_api.py <email> <password>")
        print("\nExample:")
        print("  python create_chat_rooms_api.py user@example.com mypassword")
        print()
        print("Or enter credentials now:")
        email = input("Email: ").strip()
        password = input("Password: ").strip()
    
    if not email or not password:
        print("ERROR: Email and password are required")
        sys.exit(1)
    
    create_chat_rooms(email, password)
    
    print("\nDone! You can now see these rooms in the app.")

