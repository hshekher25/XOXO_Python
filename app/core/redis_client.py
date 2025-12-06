import redis
from app.core.config import settings
from typing import Optional

# Make Redis optional - will be None if not configured or connection fails
redis_client: Optional[redis.Redis] = None

# Only try to connect if REDIS_URL is explicitly set and not empty
# Redis is completely optional - if not configured, it's silently disabled
# Skip default localhost values - user must explicitly configure Redis if they want it
redis_url = settings.REDIS_URL
if redis_url and isinstance(redis_url, str):
    redis_url = redis_url.strip()
    # Skip if empty or default localhost value (user hasn't configured it)
    if redis_url and redis_url not in ["redis://localhost:6379", "redis://127.0.0.1:6379", ""]:
        try:
            redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            redis_client.ping()
            print("✓ Redis connected successfully")
        except Exception as e:
            print(f"⚠ Redis connection failed (optional service): {e}")
            redis_client = None
# If REDIS_URL is not set, empty, or default value, Redis is disabled silently (no messages)


def is_redis_available() -> bool:
    """Check if Redis is available"""
    if redis_client is None:
        return False
    try:
        redis_client.ping()
        return True
    except:
        return False
