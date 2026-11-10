import os


from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()

class DatabaseManager:

    def __init__(self):
        self.pool: AsyncConnectionPool | None = None

    async def init_database(self):

        DB_NAME = os.getenv("DB_NAME")
        DB_HOST = os.getenv("DB_HOST")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_USER = os.getenv("DB_USER")
        DB_PORT = os.getenv("DB_PORT")

        
        self.pool =  AsyncConnectionPool(
            f"dbname={DB_NAME} user={DB_USER} host={DB_HOST} password={DB_PASSWORD} port={DB_PORT}",
            min_size=5,max_size=10,
            open=False
        )

        await self.pool.open()
    
    async def close_database(self):

        if self.pool:
            await self.pool.close()

database_manager = DatabaseManager()

