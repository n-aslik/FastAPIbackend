import asyncio
import psycopg

async def create_db():
    db = await psycopg.AsyncConnection.connect(
        "postgresql://username:@@sl8998@localhost/bookblogdb"
    )
    return db

        
