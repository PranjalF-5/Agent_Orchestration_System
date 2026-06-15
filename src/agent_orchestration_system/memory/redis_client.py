import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create a connection pool to avoid opening/closing connections repeatedly
pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

def get_redis_client() -> redis.Redis:
    """Returns an async Redis client."""
    return redis.Redis(connection_pool=pool)

async def ping_redis() -> bool:
    """Utility to test if Redis is up and responding."""
    client = get_redis_client()
    try:
        response = await client.ping()
        return response
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return False
