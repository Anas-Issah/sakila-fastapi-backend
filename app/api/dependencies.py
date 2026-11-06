
from redis.exceptions import ConnectionError
from app.core.redis_config import redis_manager
from app.database.connection import database_manager
from psycopg.errors import Error as DatabaseError


async def get_redis():

    if redis_manager.client is None:
        raise ConnectionError

    return redis_manager.client


async def get_db():

    if not database_manager.pool:
        raise DatabaseError

    async with database_manager.pool.connection() as conn:
        yield conn 
