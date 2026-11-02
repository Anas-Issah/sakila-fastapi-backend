import redis.asyncio as aioredis
import os

class RedisManager:
    def __init__(self):
        self.client: aioredis.Redis | None = None

    def init_redis(self):
        """Creates the global connection pool."""
  
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        
        self.client = aioredis.Redis(
            host=redis_host, 
            port=redis_port, 
            decode_responses=True
        )
        return self.client

    async def close_redis(self):

        if self.client:
            await self.client.aclose()


redis_manager = RedisManager()
