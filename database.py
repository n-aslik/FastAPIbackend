from psycopg_pool import AsyncConnectionPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+async://postgres:@@sl8998@localhost:5432/bookblogdb")

# Создание пула соединений
db_pool = AsyncConnectionPool(DATABASE_URL)

async def get_db_connection():
    async with db_pool.connection() as conn:
        yield conn


        
